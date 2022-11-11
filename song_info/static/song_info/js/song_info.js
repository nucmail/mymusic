window.onload = function(){
    var s = document.getElementById("pingStar");
        m = document.getElementById("dir"),
        n = s.getElementsByTagName("li"),
        input = document.getElementById("startP");//保存所选值
    clearAll = function(){
        for(var i = 0;i < n.length;i++){
            n[i].className = "";
        }
    }
    for(var i = 0;i < n.length;i++){
        n[i].onclick = function(){
            var q = this.getAttribute("rel");
            clearAll();
            input.value = q;
            for(var i = 0;i < q;i++){
                n[i].className = "on";
            }
            m.innerHTML = this.getAttribute("title");
        }
        n[i].onmouseover = function(){
            var q = this.getAttribute("rel");
            clearAll();
            for(var i = 0;i < q;i++){
                n[i].className = "on";
            }
            //m.innerHTML = this.getAttribute("title");


        }
        n[i].onmouseout = function(){
            clearAll();
            for(var i = 0;i < input.value;i++){
                n[i].className = "on";
            }
            var q = this.getAttribute("rel");

            //m.innerHTML = this.getAttribute("title");
        }
    }

}
