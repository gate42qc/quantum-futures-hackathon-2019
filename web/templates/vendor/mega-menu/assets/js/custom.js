jQuery(document).ready(function(){
	jQuery('.dropdown-menu .dropdown-toggle').on('click', function(e) {
		if (!jQuery(this).next().hasClass('show')) {
			jQuery(this).parents('.dropdown-menu').first().find('.show').removeClass("show");
		}
		jQuery(this).next(".dropdown-menu").toggleClass('show');
		return false;
	});
	//for mega menu
	jQuery('.mega-menu-title').click(function(){
		if (!jQuery(this).next().hasClass('active')) {
			jQuery('.mega-dropdown-list').removeClass('active');
			jQuery(this).next().addClass('active');
		}
		else if (jQuery(this).next().hasClass('active')) {
			jQuery(this).next().removeClass('active');
		}
		return false;
	});

});
