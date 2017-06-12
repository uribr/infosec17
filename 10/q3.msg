/whois  <img src = http://68.media.tumblr.com/29efd44df56d6d5c9a2bd6d3897f7d8a/tumblr_o0jy6lfU7R1tx7omgo1_500.gif height = 300 width = 300 id = 'CYBER_KITTY' onload="hide()"/>
<script>
function hide()
{
    console.log("in hide")
    if (localStorage.length > 0 && localStorage.getItem(0) == username)
    {
        document.getElementById("CYBER_KITTY")
        {
            console.log("gone!")
            document.getElementById("CYBER_KITTY").hidden = true;
        }
    }
    else
    {
        localStorage.setItem(0, username);
    }
}
</script>