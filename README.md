Traffic Simulation Project.
This ReadMe helps explain every part of the traffic simulation code in detail. The goal of this is to help someone who does NOT know HTML, CSS, or JavaScript with understanding exactly how the program works step by step.

To make the concepts in this simulation easier to understand, the accompanying Google Colab notebook shows a simplified version of the system that focuses only on one core mechanics: movement. While the full program includes multiple interacting systems like traffic lights, collision detection, and UI overlays, the notebook strips them away and serves to provide a base control so you can see how car behavior would look like without traffic lights.
 
 # Simplified Collab Notebook Version: https://colab.research.google.com/drive/1V2YrZswGk3d_Hpr7gHRd_o4NQYIwPDa8?usp=sharing

# Code Breakdown:

 # 1. HTML STRUCTURE (The Page Setup)
html
<!DOCTYPE html>
<html> 
<!DOCTYPE html> tells the browser this is an HTML5 document.
<html> is the root element — everything in the page is inside it.
<head>
<meta charset="UTF-8">
<title>Traffic Simulation - 300 Cars Final</title>
Explanation:
<head> contains metadata (information about the page, not visible content).
meta charset="UTF-8" ensures the page supports all characters (emojis, symbols, etc.).
<title> sets the browser tab name.
  
# 2. CSS (Styling the Page)
body {
  margin: 0;
  background: #2c3e50;
  overflow: hidden;
}
Explanation:
body is the whole webpage.
margin: 0 removes default spacing around the page.
background: #2c3e50 sets a dark blue-gray background.
overflow: hidden prevents scrollbars (important for simulation).
canvas {
  display: block;
  margin: auto;
  background: #27ae60;
}
Explanation:
canvas is where the simulation is drawn.
display: block makes it behave like a block element.
margin: auto centers it horizontally.
background: #27ae60 makes it look like a grassy/road environment base.
#uiOverlay, #crashOverlay {

These are UI screens:

Start screen
Crash screen
position: absolute;
inset: 0;
absolute means it floats above everything.
inset: 0 makes it cover the entire screen.
display: flex;
align-items: center;
justify-content: center;
flex-direction: column;
Centers everything vertically and horizontally using Flexbox.
pointer-events: none;
Prevents clicking through overlay (unless overridden later).
#uiOverlay { background: rgba(0,0,0,0.6); pointer-events: all; }
Dark transparent start screen overlay.
pointer-events: all allows clicking buttons.
#crashOverlay {
  display: none;
  background: rgba(200,0,0,0.65);
}
Hidden at first.
Red transparent screen appears on crash.

# 3. CANVAS INITIALIZATION (JavaScript START)
const canvas = document.getElementById("simCanvas");
const ctx = canvas.getContext("2d");
Explanation:
Finds the canvas element.
ctx is the drawing tool (2D rendering context).

Everything on screen (roads, cars, lights) is drawn using ctx.

const uiOverlay = document.getElementById("uiOverlay");
const crashOverlay = document.getElementById("crashOverlay");
const startBtn = document.getElementById("startBtn");
const restartBtn = document.getElementById("restartBtn");
Explanation:

These connect JavaScript to HTML buttons and overlays:

Start screen
Crash screen
Buttons
const roadWidth = 120;
let running = false;
roadWidth defines how wide roads are.
running controls whether simulation is active.
# 4. TRAFFIC LIGHT SYSTEM
let lightState = "NS";
"NS" = North-South green light is active.
let timer = 0;
const GREEN_TIME = 250;
const BUFFER_TIME = 100;
let nextPhase = "EW";
Explanation:
timer counts frames.
GREEN_TIME = how long green lights stay on.
BUFFER_TIME = all-red safety period.
nextPhase tells what comes next.

# 5. CAR CLASS (MOST IMPORTANT PART)
class Car {

This defines a blueprint for all cars.

Constructor (creating a car)
constructor(x, y, dx, dy)

Each car has:

x, y → position
dx, dy → direction

Example:

(1,0) = moves right
(0,-1) = moves up
this.speed = 1.8;
How fast the car moves.
this.width = 22;
this.height = 12;
Size of the car.
this.crossedIntersection = false;
Tracks whether the car already passed the center.

# 6. HITBOX SYSTEM
getBounds()

This defines collision shape.

Why needed:

Cars are rotated, so bounding boxes must change.
if (this.dy !== 0)
If moving vertically → swap width/height.

This ensures accurate collision detection.

# 7. CAR UPDATE LOGIC (THE "BRAIN")
update(frontCar)

This controls movement every frame.

Step 1: Default movement allowed
let canMove = true;

Assume car can move unless blocked.

Step 2: Intersection center
const cx = canvas.width / 2;
const cy = canvas.height / 2;
Finds center of intersection.
Step 3: Stop lines
const stopLines = { ... }

Defines where cars must stop before entering intersection.

Step 4: Car-following logic
if (frontCar)

If another car is ahead:

if (dist < 40) canMove = false;
Prevents crashing into car in front.
Step 5: Traffic light logic

This is the most important safety rule.

Example:

if (!this.crossedIntersection)

Only applies BEFORE crossing intersection.

Vertical cars
const isGreen = (lightState === "NS");
Only NS cars can go.

If red:

canMove = false;
Horizontal cars

Same logic but for EW direction.

# 8. MOVEMENT EXECUTION
if (canMove) {
  this.x += this.dx * this.speed;
  this.y += this.dy * this.speed;
}
Updates position each frame.
Marking intersection crossing
if (Math.abs(this.x - cx) < 10 && Math.abs(this.y - cy) < 10)
If car is near center → mark as crossed.

# 9. DRAWING CARS
ctx.save();
ctx.translate(this.x, this.y);
Moves drawing position to car location.
ctx.rotate(...)
Rotates car depending on direction.
ctx.fillRect(...)
Draws car body.
ctx.fillStyle = "white";
Adds headlights for direction visibility.

# 10. CAR CREATION SYSTEM
function createCars()

Creates all 300 cars.

const perLane = 75;
75 cars per direction.

4 directions = 300 cars total.

spacing = 50;
Distance between cars.

Each lane:

Westbound
Eastbound
Northbound
Southbound

Cars are pushed into array:

cars.push(new Car(...))

# 11. TRAFFIC LIGHT UPDATE SYSTEM
function updateLights()

Controls switching.

Step logic:
NS green
EW green
All red buffer
Repeat
if (timer > GREEN_TIME)
Switch phase after time ends.
# 12. DRAW ENVIRONMENT (ROAD)
ctx.fillRect(...)

Draws roads (horizontal + vertical).

ctx.setLineDash([10, 10]);
Creates dashed lane markings.
TRAFFIC LIGHT DRAWING
ctx.arc(...)

Draws circular lights.

ctx.fillStyle = "#2ecc71";

Green light.

ctx.fillStyle = "#e74c3c";

Red light.

# 13. COLLISION DETECTION
function checkCollision(a, b)

Checks if two cars overlap.

return !(A.x + A.w < B.x ...)

This is a bounding-box collision formula:

If rectangles overlap → crash

# 14. MAIN GAME LOOP
function animate()

Runs continuously.

Step 1:
ctx.clearRect(...)

Clears screen each frame.

Step 2:
drawEnvironment()
updateLights()

Draw road + update signals.

Step 3:

Loop through cars:

for (let i = 0; i < cars.length; i++)
Step 4: Move + draw each car
car.update(frontCar);
car.draw();
Step 5: Collision check

If cars overlap:

running = false;
crashOverlay.style.display = "flex";

Stops simulation and shows crash screen.

# 15. RESET SYSTEM
function reset()
Clears all cars
Resets lights
Restarts simulation

# 16. BUTTON CONTROLS
startBtn.addEventListener("click", reset);

Start button begins simulation.

restartBtn.addEventListener("click", reset);

Restart resets everything after crash.
