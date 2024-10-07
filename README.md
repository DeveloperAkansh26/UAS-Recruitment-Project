a# UAS-Recruitment-Project
### Task: 
The theme for this task is Search and Rescue. A fire has broken out in a civilian area and your job is to gather information about the location of houses and buildings in the area. Your UAV is collecting images of the search area that look like the sample image given below. 
###### Information about the input image:
•	The brown area is burnt grass 
•	The green area is unburnt (green) grass 
•	The blue and red triangles are houses 
•	Each house colour has an associated priority 
•	Blue house have a priority of 2 
•	Red houses have a priority of 1 
###### Expected Output: 
1.	An output image, for each input image, that clearly shows the difference between the burnt grass and green grass, by overlaying 2 unique colors on top of each. The expected output for the given sample input is given below 
2.	The number of houses on the burnt grass (Hb) and the number of houses on the green grass (Hg), saved in a list 
3.	The total priority of houses on the burnt grass (Pb) and the total priority of houses on the green grass (Pg), saved in a list .
4.	A rescue ratio of priority Pr where Pr = Pb / Pg , saved in a list 
5.	A list of the names of the input images , arranges in descending order of their rescue ratio (Pr).

### Report:
Using OpenCV and Python, I have managed to create a program that the performs the given task.
It takes in input of all the pictures stored on the device and outputs the following: n_houses, priority_house, priority_ratio and Output Image.

All the images are taken as input through a loop and all the processing for each image is done using a function names ‘result’ which returns all the output in form of lists.
The ‘result’ function using techniques like Blurring to preprocess the image for analysis.

Then a mask for the Burnt Grass region of the image is produced using the inRange() function and the obtained mask is processed using the Morphological Operations like Opening, Dilation and Erosion to obtain a mask containing the Burnt Grass and all the houses present in that area. This is used to find the mask for Green Grass region using bitwise_not operation.
  
Now to find the no. of Red and Blue houses in each regions, the masks obtained are applied to the original image to extract the regions separately.
These are used to find the Red color and Blue color houses in the images separately and further used to apply contour detection technique to identify the no. of each houses which are then stored in a dictionary.

The output image to be produced is done using image subtraction operation to get the mask of regions of Burnt and Green Grass without the houses. These are used to apply as mask to a plane solid color image. Two images obtained are combined together. 
Similarly the house masks for each region are combined together and those are used to extract the houses from the original image. Both the images are combined to form the output image.

Finally, the calculations are performed using the count dictionary created and returned in form of list required.
