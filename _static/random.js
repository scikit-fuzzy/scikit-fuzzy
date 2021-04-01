
   function insert_gallery() {
       var images = [];
       var links = [];

       ix = Math.floor(Math.random() * images.length);
       document.write(
'<div class="gallery_image">      <a href="URL"><img src="IMG"/></a></div>'.replace('IMG', images[ix]).replace('URL', links[ix])
       );

       console.log('<div class="gallery_image">      <a href="URL"><img src="IMG"/></a></div>'.replace('IMG', images[ix]).replace('URL', links[ix]));
   };

