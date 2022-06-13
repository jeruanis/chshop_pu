// some scripts
// jquery ready start
$(document).ready(function() {
	// jQuery code

    /* ///////////////////////////////////////

    THESE FOLLOWING SCRIPTS ONLY FOR BASIC USAGE,
    For sliders, interactions and other

    */ ///////////////////////////////////////

	//////////////////////// Prevent closing from click inside dropdown
    $(document).on('click', '.dropdown-menu', function (e) {
      e.stopPropagation();
    });


    $('.js-check :radio').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $('input[name='+ check_attr_name +']').closest('.js-check').removeClass('active');
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');

        } else {
            item.removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });

    $('.js-check :checkbox').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');
        } else {
            $(this).closest('.js-check').removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });

	//////////////////////// Bootstrap tooltip
	if($('[data-toggle="tooltip"]').length>0) {  // check if element exists
		$('[data-toggle="tooltip"]').tooltip()
	} // end if


  setTimeout(function(){
    $('#message').fadeOut();
  }, 3600);

  const infinite = new Waypoint.Infinite({
     element: $('.infinite-container')[0],
     onBeforePageLoad: function () {
       $('#prod_page_loading').removeClass('d-none');
     },
     onAfterPageLoad: function ($items) {
       $('#prod_page_loading').addClass('d-none');
     }
   });

  $('.store-cat').fadeOut();
  $('.thumb a').click(function(e){
    e.preventDefault();
    $('.mainimage img').attr('src', $(this).attr("href"));
  })

});
// jquery end

function displayLoadingSpinner(isDisplayed){
  var spinner = document.getElementById("id_loading_spinner")
  if(isDisplayed){
    spinner.style.display = "block"
  }
  else{
    spinner.style.display = "none"
  }
}

//login eye
const log = function() {
  const togglePassword = document.querySelector('#togglePassword');
  const password = document.querySelector('#id_password');
  togglePassword.addEventListener('click', function (e) {
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    this.classList.toggle('fa-eye-slash');
  });
}

//register eye
const reg = function() {
  const togglePassword = document.querySelector('#togglePassword');
  const togglePassword2 = document.querySelector('#togglePassword2');
  const password = document.querySelector('#id_password');
  const password2 = document.querySelector('#id_confirm_password');
  togglePassword.addEventListener('click', function (e) {
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    this.classList.toggle('fa-eye-slash');
  });
    togglePassword2.addEventListener('click', function (e) {
      const type = password2.getAttribute('type') === 'password' ? 'text' : 'password';
      password2.setAttribute('type', type);
      this.classList.toggle('fa-eye-slash');
  });
}

//for home banner
const br_ht = function() {
  if(window.matchMedia("(min-width:600px)").matches){
    $(".banr").css({"height":"415px"});
  }else{
    $(".banr_in").css({"height":"260px"})
  }
}

function getLiveSearch(value, url) {
		$.ajax({
			url:url,
			type: "GET",
			data:{'keyword':value},
			cache:false,
			"success": function(data, textStatus){
				$('#search_result').html(data['html_from_view']);
			},
		});
	 }
 $(function(){
	 br_ht();
 })
