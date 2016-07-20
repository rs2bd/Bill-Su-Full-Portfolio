






$.ajax({
 url : "6912.dot",
 success : function(dot_str){
  var container = document.getElementById('graph');
  var graph = new vis.Graph(container, {dot: dot_str}, options);
 }
});