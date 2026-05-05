Table fragments;
ArrayList<Spark> sparks = new ArrayList<Spark>();

float globalScale = 6.0;

void setup() {
  size(1280, 720, P3D);
  frameRate(30);
  smooth(8);
  fragments = loadTable("emotion_city_fragments_32.csv", "header");

  for (int i = 0; i < 360; i++) {
    sparks.add(new Spark(i));
  }
}

void draw() {
  float t = frameCount / 30.0;
  drawAtmosphere(t);

  hint(ENABLE_DEPTH_TEST);
  ambientLight(24, 26, 35);
  directionalLight(120, 140, 190, -0.3, 0.5, -0.6);
  pointLight(255, 95, 70, sin(t * 0.7) * 260, -260, cos(t * 0.5) * 260);
  pointLight(60, 180, 255, cos(t * 0.4) * 320, -220, sin(t * 0.6) * 320);

  float camRadius = 265 + sin(t * 0.18) * 38;
  camera(
    sin(t * 0.10) * camRadius,
    -185 + sin(t * 0.23) * 28,
    cos(t * 0.10) * camRadius,
    0, -55, 0,
    0, 1, 0
  );

  pushMatrix();
  rotateX(-0.58);
  translate(0, 95, 0);
  scale(globalScale);

  drawEnergyGrid(t);
  drawConnections(t);

  for (int i = 0; i < fragments.getRowCount(); i++) {
    drawFragment(fragments.getRow(i), i, t);
  }

  for (Spark s : sparks) {
    s.update(t);
    s.display(t);
  }

  popMatrix();
  drawOverlay(t);
}

void drawAtmosphere(float t) {
  hint(DISABLE_DEPTH_TEST);
  noStroke();
  for (int y = 0; y < height; y += 3) {
    float amt = map(y, 0, height, 0, 1);
    float r = lerp(28, 58, amt);
    float g = lerp(34, 48, amt);
    float b = lerp(62, 78, amt);
    fill(r, g, b);
    rect(0, y, width, 3);
  }

  blendMode(ADD);
  for (int i = 0; i < 6; i++) {
    float x = width * (0.2 + 0.6 * noise(i * 10.0, t * 0.05));
    float y = height * (0.2 + 0.5 * noise(i * 20.0, t * 0.04));
    float rad = 180 + 90 * noise(i, t * 0.07);
    fill(i % 2 == 0 ? color(45, 165, 255, 10) : color(255, 110, 70, 9));
    ellipse(x, y, rad * 0.72, rad * 0.72);
  }
  blendMode(BLEND);
  hint(ENABLE_DEPTH_TEST);
}

void drawEnergyGrid(float t) {
  strokeWeight(0.45);
  for (int i = -70; i <= 70; i += 5) {
    float wave = sin(t * 1.4 + i * 0.2) * 1.5;
    stroke(90, 205, 255, 125);
    line(i, wave, -70, i, -wave, 70);
    stroke(255, 135, 82, 95);
    line(-70, -wave, i, 70, wave, i);
  }

  noFill();
  for (int ring = 16; ring <= 72; ring += 14) {
    stroke(140, 220, 255, 76 - ring * 0.45);
    pushMatrix();
    rotateY(t * 0.08 + ring);
    ellipse(0, 0, ring * 2, ring * 2);
    popMatrix();
  }
}

void drawConnections(float t) {
  strokeWeight(0.65);
  for (int i = 0; i < fragments.getRowCount(); i++) {
    TableRow a = fragments.getRow(i);
    TableRow b = fragments.getRow((i + 3) % fragments.getRowCount());
    float ax = a.getFloat("scene_x");
    float az = a.getFloat("scene_z");
    float bx = b.getFloat("scene_x");
    float bz = b.getFloat("scene_z");
    float ar = a.getFloat("red") * 255;
    float ag = a.getFloat("green") * 255;
    float ab = a.getFloat("blue") * 255;
    float alpha = 70 + 45 * sin(t * 1.2 + i * 0.31);
    stroke(min(255, ar + 45), min(255, ag + 45), min(255, ab + 45), alpha);
    line(ax, -4, az, bx, -4, bz);
  }
}

void drawFragment(TableRow row, int i, float t) {
  float x = row.getFloat("scene_x");
  float z = row.getFloat("scene_z");
  float h = row.getFloat("height");
  float w = row.getFloat("width");
  float d = row.getFloat("depth");
  float distortion = row.getFloat("distortion");
  float speed = row.getFloat("movement_speed");
  float rot = row.getFloat("rotation_speed");
  float r = row.getFloat("red") * 255;
  float g = row.getFloat("green") * 255;
  float b = row.getFloat("blue") * 255;
  boolean stress = row.getString("category").indexOf("commercial") >= 0;

  float pulse = sin(t * speed * 2.0 + i * 0.7) * distortion;
  float jitterX = stress ? sin(t * 5.0 + i) * distortion * 0.35 : sin(t * 0.8 + i) * distortion * 0.12;
  float jitterZ = stress ? cos(t * 4.4 + i) * distortion * 0.35 : cos(t * 0.7 + i) * distortion * 0.12;

  pushMatrix();
  translate(x + jitterX, -h / 2 - pulse, z + jitterZ);
  rotateY(t * rot * 35 + i * 0.08);
  rotateX(sin(t * 0.6 + i) * distortion * 0.01);

  blendMode(ADD);
  noStroke();
  fill(min(255, r + 40), min(255, g + 40), min(255, b + 40), stress ? 70 : 52);
  box(w * 1.65, max(2, h + pulse) * 1.08, d * 1.65);
  blendMode(BLEND);

  stroke(min(255, r + 70), min(255, g + 70), min(255, b + 70), 255);
  strokeWeight(stress ? 1.15 : 0.85);
  fill(min(255, r + 34), min(255, g + 34), min(255, b + 34), stress ? 185 : 155);
  box(w, max(2, h + pulse), d);

  stroke(255, 255, 255, stress ? 165 : 115);
  noFill();
  box(w * 1.16, max(2, h + pulse) * 1.03, d * 1.16);

  drawRibs(w, d, h + pulse, r, g, b, stress);
  popMatrix();
}

void drawRibs(float w, float d, float h, float r, float g, float b, boolean stress) {
  int count = stress ? 7 : 4;
  stroke(min(255, r + 80), min(255, g + 80), min(255, b + 80), stress ? 220 : 155);
  strokeWeight(0.72);
  for (int j = 1; j < count; j++) {
    float y = map(j, 0, count, -h / 2, h / 2);
    line(-w / 2, y, -d / 2, w / 2, y, -d / 2);
    line(-w / 2, y, d / 2, w / 2, y, d / 2);
    line(-w / 2, y, -d / 2, -w / 2, y, d / 2);
    line(w / 2, y, -d / 2, w / 2, y, d / 2);
  }
}

void drawOverlay(float t) {
  hint(DISABLE_DEPTH_TEST);
  camera();
  noLights();
  fill(235, 240, 255, 220);
  textSize(18);
  text("Emotion City Map / ML fragments", 28, 38);
  textSize(12);
  fill(160, 175, 195, 190);
  text("calm-open parks  <  spatial density / stress  >  commercial fragments", 28, 60);

  float progress = (frameCount % (30 * 65)) / float(30 * 65);
  noStroke();
  fill(255, 255, 255, 30);
  rect(28, height - 38, 360, 5);
  fill(80, 180, 255, 190);
  rect(28, height - 38, 360 * progress, 5);
  hint(ENABLE_DEPTH_TEST);
}

class Spark {
  float seed;
  float radius;
  float y;
  float speed;
  color c;

  Spark(int id) {
    seed = id * 17.131;
    radius = random(20, 76);
    y = random(-46, -4);
    speed = random(0.18, 1.4);
    c = random(1) > 0.48 ? color(70, 180, 255) : color(255, 92, 48);
  }

  void update(float t) {
  }

  void display(float t) {
    float a = t * speed + seed;
    float x = cos(a) * radius + noise(seed, t * 0.2) * 18 - 9;
    float z = sin(a * 0.8) * radius + noise(seed + 4, t * 0.17) * 18 - 9;
    float yy = y + sin(t * speed + seed) * 12;
    blendMode(ADD);
    noStroke();
    fill(c, 135);
    pushMatrix();
    translate(x, yy, z);
    sphereDetail(6);
    sphere(0.9 + noise(seed, t) * 1.5);
    popMatrix();
    blendMode(BLEND);
  }
}
