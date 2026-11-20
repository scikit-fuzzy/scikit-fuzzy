"""Bounded batches for independent controller output observations."""
import numpy as np

from ..defuzzify.exceptions import EmptyMembershipError


def _linear_segments(x, mfx, moments=False):
    """Areas and first moments with the scalar formulas and branch order."""
    x, mfx = np.asarray(x), np.asarray(mfx)
    x1, x2 = x[..., :-1], x[..., 1:]
    y1, y2 = mfx[..., :-1], mfx[..., 1:]
    dx = x2 - x1
    valid = ~(((y1 == 0) & (y2 == 0)) | (x1 == x2))
    dtype = np.result_type(dx, y1, np.asarray(0.5 * dx.dtype.type(0)).dtype)
    area = np.zeros(dx.shape, dtype=dtype)
    rect = valid & (y1 == y2)
    rise = valid & ~rect & (y1 == 0) & (y2 != 0)
    fall = valid & ~rect & ~rise & (y2 == 0) & (y1 != 0)
    general = valid & ~rect & ~rise & ~fall
    area[rect] = dx[rect] * y1[rect]
    area[rise] = _scalar_scale(0.5, dx[rise]) * y2[rise]
    area[fall] = _scalar_scale(0.5, dx[fall]) * y1[fall]
    area[general] = _scalar_scale(0.5, dx[general]) * (y1[general] + y2[general])
    if not moments:
        return area, valid
    moment = np.zeros(dx.shape, dtype=dtype)
    moment[rect] = _scalar_scale(0.5, x1[rect] + x2[rect])
    moment[rise] = _scalar_scale(2.0 / 3.0, dx[rise]) + x1[rise]
    moment[fall] = _scalar_scale(1.0 / 3.0, dx[fall]) + x1[fall]
    moment[general] = ((_scalar_scale(2.0 / 3.0, dx[general])
                       * (y2[general] + _scalar_scale(0.5, y1[general])))
                      / (y1[general] + y2[general]) + x1[general])
    return area, moment, valid


def supported(calculator):
    """Use the legacy path for unsupported data and custom defuzzifiers."""
    variable, simulation = calculator.var, calculator.sim
    mode = variable.defuzzify_method.lower()
    if mode not in ('centroid', 'bisector', 'mom', 'som', 'lom'):
        return False
    x = variable.universe
    if x.ndim != 1 or x.size < 2 or not np.isfinite(x).all() or not (np.diff(x) > 0).all():
        return False
    if not simulation._array_shape or not np.prod(simulation._array_shape):
        return False
    for term in variable.terms.values():
        cut = term.membership_value[simulation]
        if (not isinstance(cut, np.ndarray) or cut.shape != simulation._array_shape
                or cut.dtype.kind not in 'fiu' or not np.isfinite(cut).all()
                or not np.isfinite(term.mf).all()):
            return False
    return bool(variable.terms)


def defuzzify(calculator):
    """Batch ragged cut universes using duplicate padding of zero-width spans."""
    variable, simulation = calculator.var, calculator.sim
    x = variable.universe
    terms = list(variable.terms.values())
    cuts = np.stack([term.membership_value[simulation].ravel() for term in terms])
    total = cuts.shape[1]
    result = np.empty(total, dtype=np.float64)
    # Crossing masks and their index scans are bounded independently of the
    # number of observations. A very large single universe is the lower bound.
    block = max(1, min(128, 131072 // max(1, len(terms) * x.size)))
    for start in range(0, total, block):
        stop = min(total, start + block)
        batch = stop - start
        masks, crossing_values = [], []
        for index, term in enumerate(terms):
            levels = cuts[index, start:stop, None]
            inside = np.where(levels == 0, term.mf > levels, term.mf >= levels)
            crossing = np.diff(inside, axis=1)
            values = np.full(crossing.shape, x[-1], dtype=float)
            rows, cols = np.nonzero(crossing)
            values[rows, cols] = (x[cols]
                                  + (levels[rows, 0] - term.mf[cols])
                                  * (x[cols + 1] - x[cols])
                                  / (term.mf[cols + 1] - term.mf[cols]))
            masks.append(crossing)
            crossing_values.append(values)
        masks = np.concatenate(masks, axis=1)
        values = np.concatenate(crossing_values, axis=1)
        count = masks.sum(axis=1)
        universe = np.full((batch, x.size + int(count.max())), x[-1], dtype=float)
        universe[:, :x.size] = x
        rows, cols = np.nonzero(masks)
        offsets = np.cumsum(masks, axis=1)[rows, cols] - 1
        universe[rows, x.size + offsets] = values[rows, cols]
        universe.sort(axis=1)
        output = np.zeros(universe.shape, dtype=float)
        for index, term in enumerate(terms):
            mf = np.interp(universe.ravel(), x, term.mf, left=0., right=0.).reshape(universe.shape)
            np.minimum(cuts[index, start:stop, None], mf, out=mf)
            np.maximum(output, mf, out=output)
        mode = variable.defuzzify_method.lower()
        if mode in ('centroid', 'bisector'):
            if np.any(output.sum(axis=1) == 0):
                raise EmptyMembershipError()
            area, moment, valid = _linear_segments(universe, output, moments=True)
            area = np.where(valid, area, 0)
            first = np.where(valid, moment * area, 0)
            zero = np.zeros((batch, 1), dtype=area.dtype)
            denominator = np.cumsum(np.concatenate((zero, area), axis=1), axis=1)[:, -1]
            numerator = np.cumsum(np.concatenate((zero, first), axis=1), axis=1)[:, -1]
            if mode == 'centroid':
                result[start:stop] = numerator / np.fmax(denominator, np.finfo(float).eps)
            else:
                cumulative = np.cumsum(np.concatenate((zero, area), axis=1), axis=1)[:, 1:]
                segment = np.argmax(cumulative >= denominator[:, None] / 2., axis=1)
                rows = np.arange(batch)
                previous = np.where(segment == 0, 0., cumulative[rows, np.maximum(segment - 1, 0)])
                remaining = denominator / 2. - previous
                x1, x2 = universe[rows, segment], universe[rows, segment + 1]
                y1, y2 = output[rows, segment], output[rows, segment + 1]
                dx = x2 - x1
                answer = np.empty(batch)
                rectangle = y1 == y2
                rise = ~rectangle & (y1 == 0)
                fall = ~rectangle & ~rise & (y2 == 0)
                general = ~rectangle & ~rise & ~fall
                answer[rectangle] = remaining[rectangle] / y1[rectangle] + x1[rectangle]
                answer[rise] = np.sqrt(2. * remaining[rise] * dx[rise] / y2[rise]) + x1[rise]
                answer[fall] = (x2[fall] - np.sqrt(dx[fall] * dx[fall]
                                                 - 2. * remaining[fall] * dx[fall] / y1[fall]))
                slope = (y2[general] - y1[general]) / dx[general]
                root = np.sqrt(y1[general] * y1[general] + 2. * slope * remaining[general])
                answer[general] = x1[general] - (y1[general] - root) / slope
                result[start:stop] = answer
        else:
            unique = np.concatenate((np.ones((batch, 1), dtype=bool),
                                     np.diff(universe, axis=1) != 0), axis=1)
            maxima = (output == output.max(axis=1, keepdims=True)) & unique
            if mode == 'mom':
                # Count each peak coordinate once despite duplicate padding.
                result[start:stop] = np.where(maxima, universe, 0.).sum(axis=1) / maxima.sum(axis=1)
            elif mode == 'som':
                result[start:stop] = np.where(maxima, universe, np.inf).min(axis=1)
            else:
                result[start:stop] = np.where(maxima, universe, -np.inf).max(axis=1)
    # The legacy per-observation path leaves these private values at the last
    # observation. Preserve that diagnostic state as well as the output.
    for index, term in enumerate(terms):
        term._cut = cuts[index, -1]
    return result.reshape(simulation._array_shape)



def _scalar_scale(factor, values):
    """Match Python float times NumPy scalar promotion on NumPy 1 and 2."""
    dtype = np.asarray(factor * values.dtype.type(0)).dtype
    return np.multiply(factor, values, dtype=dtype)
