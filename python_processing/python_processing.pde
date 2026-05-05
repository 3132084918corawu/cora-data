Table data;

float currentEmotion = 0.1;
float currentDensity = 0.05;

void setup() {
  size(1000, 800, P3D);
  smooth(8);
  frameRate(30);
  data = loadTable("emotion_dataset.csv", "header");
}

void draw() {
  float targetEmotion = map(mouseX, 0, width, 0.1, 1.0);
  float targetDensity = map(mouseX, 0, width, 0.05, 1.0);

  targetEmotion = constrain(targetEmotion, 0.1, 1.0);
  targetDensity = constrain(targetDensity, 0.05, 1.0);

  currentEmotion = lerp(currentEmotion, targetEmotion, 0.11);
  currentDensity = lerp(currentDensity, targetDensity, 0.11);

  drawBackground(currentEmotion);
  drawInterface(currentEmotion, currentDensity);

  lights();
  ambientLight(92, 98, 108);
  directionalLight(215, 210, 200, -0.3, 0.55, -0.6);
  pointLight(90, 150, 210, 260, -220, 180);
  pointLight(210, 115, 78, -260, -180, -120);

  translate(width / 2, height * 0.63, -80);
  rotateX(-0.62);
  rotateY(frameCount * 0.018);

  drawGround(currentEmotion, currentDensity);
  drawEmotionCity(currentEmotion, currentDensity);
  drawEmotionRings(currentEmotion);
}

void drawBackground(float emotion) {
  for (int y = 0; y < height; y += 2) {
    float amt = map(y, 0, height, 0, 1);

    float calmR = lerp(226, 245, amt);
    float calmG = lerp(242, 250, amt);
    float calmB = lerp(252, 255, amt);

    float stressR = lerp(255, 248, amt);
    float stressG = lerp(235, 218, amt);
    float stressB = lerp(220, 210, amt);

    float r = lerp(calmR, stressR, emotion);
    float g = lerp(calmG, stressG, emotion);
    float b = lerp(calmB, stressB, emotion);

    stroke(r, g, b);
    line(0, y, width, y);
  }

  noStroke();
  blendMode(ADD);
  fill(80, 180, 255, 28);
  ellipse(width * 0.28, height * 0.32, 420, 280);
  fill(255, 120, 70, 24 * emotion);
  ellipse(width * 0.68, height * 0.36, 430, 300);
  blendMode(BLEND);
}

void drawInterface(float emotion, float density) {
  hint(DISABLE_DEPTH_TEST);
  camera();
  noLights();

  fill(20, 24, 32, 230);
  textSize(20);
  text("Emotion Generated City", 30, 38);

  textSize(14);
  fill(35, 45, 60, 210);
  text("Move mouse left = Park / Relaxed / Open", 30, 66);
  text("Move mouse right = Commercial / Stressful / Dense", 30, 88);

  noStroke();
  fill(20, 30, 45, 35);
  rect(30, 112, 340, 10, 6);

  float knobX = map(emotion, 0.1, 1.0, 30, 370);
  fill(70, 180, 255, 210);
  rect(30, 112, knobX - 30, 10, 6);
  fill(255, 118, 70, 220);
  ellipse(knobX, 117, 20, 20);

  fill(35, 45, 60, 210);
  text("emotion: " + nf(emotion, 1, 2) + "    density: " + nf(density, 1, 2), 30, 148);
  hint(ENABLE_DEPTH_TEST);
}

void drawGround(float emotion, float density) {
  float gridSize = 720;
  float step = map(density, 0, 1, 72, 38);

  strokeWeight(1);
  for (float i = -gridSize / 2; i <= gridSize / 2; i += step) {
    float alpha = map(abs(i), 0, gridSize / 2, 120, 25);
    stroke(lerp(80, 255, emotion), lerp(170, 120, emotion), lerp(220, 90, emotion), alpha);
    line(i, 0, -gridSize / 2, i, 0, gridSize / 2);
    line(-gridSize / 2, 0, i, gridSize / 2, 0, i);
  }

  noFill();
  strokeWeight(1.6);
  for (int r = 120; r <= 420; r += 100) {
    stroke(60, 140, 210, 36);
    ellipse(0, 0, r, r);
  }
}

void drawEmotionCity(float emotion, float density) {
  int grid = 8;
  float spacing = map(density, 0, 1, 78, 35);
  float boxSize = map(density, 0, 1, 22, 58);
  float distortion = map(emotion, 0, 1, 4, 62);
  float heightFactor = map(emotion, 0, 1, 70, 265);

  float r = map(emotion, 0, 1, 45, 255);
  float g = map(emotion, 0, 1, 170, 105);
  float b = map(emotion, 0, 1, 245, 65);

  for (int x = -grid; x <= grid; x++) {
    for (int z = -grid; z <= grid; z++) {
      float distFromCentre = dist(x, z, 0, 0);
      float falloff = map(distFromCentre, 0, grid * 1.4, 1.1, 0.45);
      falloff = constrain(falloff, 0.35, 1.1);

      float localNoise = noise(x * 0.22, z * 0.22, frameCount * 0.026);
      float pulse = sin(frameCount * 0.12 + x * 0.4 + z * 0.35) * map(emotion, 0, 1, 10, 36);
      float h = max(8, heightFactor * localNoise * falloff + pulse);

      float stressJitter = map(emotion, 0, 1, 0.3, 1.0);
      float offsetX = sin(frameCount * 0.082 + x * 0.9) * distortion * stressJitter;
      float offsetZ = cos(frameCount * 0.082 + z * 0.9) * distortion * stressJitter;

      float px = x * spacing + offsetX;
      float pz = z * spacing + offsetZ;

      pushMatrix();
      translate(px, -h / 2, pz);
      rotateY(frameCount * 0.012 * emotion + (x + z) * 0.015);

      blendMode(BLEND);
      noStroke();
      fill(r, g, b, map(emotion, 0, 1, 18, 32));
      box(boxSize * 1.22, h * 1.03, boxSize * 1.22);
      blendMode(BLEND);

      stroke(max(0, r - 35), max(0, g - 35), max(0, b - 35), 235);
      strokeWeight(1.15);
      fill(r * 0.82, g * 0.82, b * 0.82, map(emotion, 0, 1, 135, 190));
      box(boxSize, h, boxSize);

      stroke(25, 35, 48, 125);
      noFill();
      box(boxSize * 1.08, h * 1.02, boxSize * 1.08);

      popMatrix();

      if ((x + z + frameCount / 20) % 4 == 0) {
        drawVerticalTrace(px, pz, h, r, g, b);
      }
    }
  }
}

void drawVerticalTrace(float x, float z, float h, float r, float g, float b) {
  stroke(r, g, b, 105);
  strokeWeight(0.8);
  line(x, -h - 30, z, x, -h - 115, z);
}

void drawEmotionRings(float emotion) {
  noFill();
  strokeWeight(2);

  for (int i = 0; i < 4; i++) {
    float radius = 170 + i * 75 + sin(frameCount * 0.07 + i) * 26;
    float alpha = map(i, 0, 3, 80, 20);
    stroke(lerp(40, 255, emotion), lerp(170, 110, emotion), lerp(245, 70, emotion), alpha);

    pushMatrix();
    rotateY(frameCount * 0.018 + i * 0.4);
    ellipse(0, -18 - i * 8, radius, radius * 0.62);
    popMatrix();
  }
}
