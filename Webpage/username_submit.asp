<!DOCTYPE html>
<html>

	<head>
		<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js">
		</script>
		<script src="brain-0.6.3.js"
<script>
function trainNetwork()
{
	var net = new brain.NeuralNetwork();
	net.train([{input: { p1: 1, p2: 2}, output: { blue: 1}},
			   {input: { p1: 0, p2: 2}, output: { blue: 1}},
			   {input: { p1: 0.5, p2: 2}, output: { blue: 0}}]);
}

function testInput()
{
	var output = net.run({ p1: 0, p2: 1});
}




</script>
    <link rel="shortcut icon" href="LoL.ico">
		<title> LoL Game Prediction </title>
		<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script><link rel="stylesheet"
		href="http://netdna.bootstrapcdn.com/bootstrap/3.0.2/css/bootstrap.min.css" rel="stylesheet">		
    <link rel="stylesheet" href="styles.css">

		<style>
		</style>

	</head>

	<body>
     <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container">
        <div class="navbar-header">
          <a class="navbar-brand" href="mainpage.html">PredictLeague</a>
        </div>
        <div class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li class="active"><a href="mainpage.html">Home</a></li>
            <li><a href="about.html">About</a></li>
            <li><a href="approach.html">Approach</a></li>
            <li><a href="results.html">Results</a></li>
            <li><a href="codeDictionary.html">Code Dictionary</a></li>
            <li><a href="presentation.html">Presentation Slides</a></li>
            <li><a href="contact.html">Contact</a></li>
          </ul>
          <form class="navbar-form navbar-left" action="mainpage.html" role="Username" method = "get">
            <div class="form-group">
              <input type="text" class="form-control" placeholder="Username" name = "username">
            </div>
          <button type="submit" class="btn btn-default">Submit</button>
          </form>
        </div><!--/.nav-collapse -->
      </div>
    </div>

    <br>
    <br>
    <br>
    

    <div class="right_adjusted_main" style="font-family: myriadPro;"> 
      <p>
        <br>
        This is the main page for my CS 152: Neural Networks final project. The intended design of this final project was to either research further into a topic we discussed in class or expand upon something we learned in class in a program. I have decided to do the latter and apply what we learned about back propagating neural networks to create a neural network to predict the victor of League of Legends games. To learn more about League of Legends in general, the process of the project, and the final results, follow the links above.
      </p>
    </div>

    <div class = "logopos">
      <img border="0" src="LeagueLogo3.jpg" alt="League Logo" width = "500">
    <div>

    <script>
    function sum(a, b) 
      return a + b;
      
    var element = $("#test");
    element.click(function() { element.slideUp(); 
    });
    </script>

	</body>
</html>
