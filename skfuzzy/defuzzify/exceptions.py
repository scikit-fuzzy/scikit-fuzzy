class DefuzzifyError(AssertionError):
    pass


class EmptyMembershipError(DefuzzifyError):
    def __init__(self):
        super().__init__("The membership function area is empty.")


class InconsistentMFDataError(DefuzzifyError):
    def __init__(self):
        super().__init__("  The lengths of the 'x' array and the fuzzy"
                         " membership function arrays are not equal.")
