

window.onload = function(){
	on_load_setting();
	
	var selectElement = document.getElementById("image-resize-selector");
	selectElement.addEventListener('change', resizeImg);
	

};

function resizeImg(e){
	const value = e.target.value;	
	const containers = document.getElementsByClassName("post_container");
	const imgs = document.querySelectorAll(".post img");


	for (var i=0; i<containers.length; i++){
		container = containers[i];
		img = imgs[i];
		
		if (value =="fit") {
			set_fit(container, img)		
		}
	
		else if (value == "sample"){
			if (img.height > img.width){
			set_sample_v(container, img)

			}
			else{
			set_sample_h(container, img)
			}

		}
	
		else if (value== "fitv"){
			set_fitv(container, img)
			} 			
	}
	
}

function on_load_setting(){
	const containers = document.getElementsByClassName("post_container");
	const imgs = document.querySelectorAll(".post img");



	for (var i=0; i<containers.length; i++){
		container = containers[i];
		img = imgs[i];	
		console.log("height", img.height);
		console.log("width", img.width);
		if (img.height > img.width){
			set_fitv(container, img);
			// console.log('onload, height');
			document.getElementById("image-resize-selector").selectedIndex = 1;

		}
		else{
			set_fit(container, img);
			// console.log('onload, width');
			document.getElementById("image-resize-selector").selectedIndex = 0;
		}


	}


}








function set_fitv(container, img){

		container.style.maxHeight = "95vh";
		container.style.maxWidth = "none"; 
		
		img.style.maxHeight = "95vh"; 
		img.style.maxWidth = "none"; 	
	}



function set_fit(container, img){

		container.style.maxHeight = "none";
		container.style.maxWidth = "100%"; 
		
		img.style.maxHeight = "none"; 
		img.style.maxWidth = "100%";  	
	
}


function set_sample_v(container, img){
	

	container.style.maxHeight = "85vh";
	container.style.maxWidth= "none";
	
	img.style.maxHeight = "85vh"; 
	img.style.maxWidth = "none"; 
	
}

function set_sample_h(container, img){

	container.style.maxHeight = "none";
	container.style.maxWidth= "850px";
	
	img.style.maxHeight = "none"; 
	img.style.maxWidth = "100%"; 
	

}