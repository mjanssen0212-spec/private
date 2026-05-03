README.txt
Exercise 1: Depth Perception in 2D
Step 1: Added Cylinder between spheres. This creates a visual overlap where one object partially hides another, confirming their relative order in space (Depth Cue: Occlusion).

Step 2: Added human models next to each sphere. By placing objects of a familiar size (human height) near the spheres, the viewer can judge the absolute size and distance of the spheres (Depth Cue: Known Size).

Step 3: Added a textured floor. A continuous surface extending into the distance provides a structural grid that anchors the objects (Depth Cue: Texture Gradient).

Step 4: Added a stripe on the ground. This reinforces the convergence of parallel lines toward a vanishing point, emphasizing the distance (Depth Cue: Linear Perspective).

Step 5: Added a cylinder below the red sphere. This connects the floating object to the ground plane, making its specific distance from the camera clearer (Depth Cue: Height in the Visual Field / Ground Contact).

Step 6: Added textures to the spheres. Detailed surfaces help the viewer perceive the volume and curvature of the objects rather than seeing them as flat circles (Depth Cue: Shading and Contour).

Step 7: Added environmental fog. Objects further away appear less distinct and slightly desaturated, simulating the effect of the atmosphere (Depth Cue: Aerial Perspective).

Step 8: Added shadows. Shadows provide information about the light source and the object's position relative to the floor, significantly grounding them in the 3D space (Depth Cue: Cast Shadows).


Further considerations not executed because they may be out of scope of the exercise: 

Remove black skybox as real sky makes Depth perception easier
Make spheres move to Show Motion paralax
Make VR camera movable to allow user to move within the scene 


Exercise 2: Depth Perception in 3D (VR)
Step 9: Replaced standard camera with Meta Camera Rig. Transitioning the scene to Virtual Reality introduces depth cues that are impossible to achieve on a 2D screen:

Binocular Disparity: The VR headset renders two slightly different images—one for each eye. The brain merges these images to calculate precise depth based on the offset (Stereopsis).

Convergence: The physical inward rotation of the eyes to focus on the nearby red sphere provides muscular feedback to the brain, signaling that the object is within close reach.

Used Assets
Invector Third Person Controller (Basic Locomotion): Used for the human scale models. Link

Low Poly Street Pack: Used for ground textures and environmental materials.