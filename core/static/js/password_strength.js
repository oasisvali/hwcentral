/*
    jQuery document ready.
*/
$(document).ready(function()
{
    /*
        assigning keyup event to password field
        so everytime user type code will execute
    */

    $('#id_new_password1').keyup(function()
    {
        $('#result').html(checkStrength($('#id_new_password1').val()))
    })  
    
    /*
        checkStrength is function which will do the 
        main password strength checking for us
    */
    
    function checkStrength(password)
    {
        //initial strength
        var strength = 0
        
        //if the password length is less than 8, return message.
        if (password.length < 8) { 
            $('#result').removeClass()
            $('#result').addClass('short')
            return 'Password is too short' 
        }
        
        //length is ok, lets continue.
        
        //if length is 8 characters or more, increase strength value
        if (password.length > 7) strength += 1

        //if length is 11 characters or more, increase strength value
        if (password.length > 10) strength += 1

        //if length is 14 characters or more, increase strength value
        if (password.length > 13) strength += 2
        
        //if length is 17 characters or more, increase strength value
        if (password.length > 16) strength += 2
        
        //if password contains both lower and uppercase characters, increase strength value
        if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/))  strength += 1
        
        //if it has numbers and characters, increase strength value
        if (password.match(/([a-zA-Z])/) && password.match(/([0-9])/))  strength += 1 
        
        //if it has one special character, increase strength value
        if (password.match(/([!,%,&,@,#,$,^,*,?,_,~])/))  strength += 1
        
        //now we have calculated strength value, we can return messages
        
        //if value is less than or equal to 3
        if (strength <= 3 )
        {
            $('#result').removeClass()
            $('#result').addClass('weak')
            return 'Password is weak'           
        }
        else if (strength >=4 && strength <=5)
        {
            $('#result').removeClass()
            $('#result').addClass('good')
            return 'Password is good'       
        }
        else
        {
            $('#result').removeClass()
            $('#result').addClass('strong')
            return 'Password is strong'
        }
    }
});