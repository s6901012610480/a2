from collections import Counter

class Trash:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = 420
        self.speed = 5
        self.landed = False

    def get_bin(self):
        return "General"

    def get_color(self):
        return color(150, 150, 150)

    def get_weight(self):
        return 0.1

    def update(self):
        if not self.landed:
            self.x += (self.target_x - self.x) * 0.12
            self.y += self.speed
            if self.y >= self.target_y:
                self.y = self.target_y
                self.landed = True

    def display(self):
        fill(self.get_color())
        stroke(40)
        strokeWeight(1.5)
        ellipse(self.x, self.y, 44, 44)
        fill(255)
        textAlign(CENTER, CENTER)
        textSize(11)
        text(self.name, self.x, self.y)


class RecyclableTrash(Trash):
    def get_bin(self):
        return "Recyclable"

    def get_color(self):
        return color(52, 152, 219)

    def get_weight(self):
        return 0.15


class OrganicTrash(Trash):
    def get_bin(self):
        return "Organic"

    def get_color(self):
        return color(46, 204, 113)

    def get_weight(self):
        return 0.25

class GeneralTrash(Trash):
    def get_bin(self):
        return "General"

    def get_color(self):
        return color(230, 126, 34)

    def get_weight(self):
        return 0.05

CATEGORY = {
    "plastic": RecyclableTrash,
    "paper": RecyclableTrash,
    "food": OrganicTrash,
    "wrapper": GeneralTrash,
}

BIN_X = {
    "Recyclable": 390,
    "Organic": 550,
    "General": 710,
}

BIN_COLOR = {
    "Recyclable": (52, 152, 219),
    "Organic": (46, 204, 113),
    "General": (230, 126, 34),
}

items_order = ["plastic", "paper", "food", "wrapper"]
select_counts = {"plastic": 2, "paper": 1, "food": 2, "wrapper": 1}

bin_tally = Counter({"Recyclable": 0, "Organic": 0, "General": 0})
total_weight = 0.0

spawn_queue = []
active_trash = []
spawn_timer = 0
status_msg = "Adjust counts and press SAVE"

def setup():
    size(850, 560)
    textFont(createFont("SansSerif", 14))

def draw():
    global spawn_timer, total_weight, status_msg
    background(242, 245, 248)
    fill(255)
    stroke(210)
    strokeWeight(1)
    rect(20, 20, 250, 520, 12)
    fill(40)
    textAlign(LEFT, TOP)
    textSize(18)
    text("Trash Selector", 40, 40)

    for i, item in enumerate(items_order):
        y_pos = 95 + i * 65
        fill(60)
        textSize(15)
        textAlign(LEFT, CENTER)
        text(item.capitalize(), 40, y_pos + 16)

        draw_button(140, y_pos, 32, 32, "-", color(231, 76, 60))
        fill(30)
        textAlign(CENTER, CENTER)
        textSize(15)
        text(str(select_counts[item]), 190, y_pos + 16)
        draw_button(208, y_pos, 32, 32, "+", color(46, 204, 113))

    draw_button(40, 370, 210, 42, "SAVE", color(52, 73, 94))
    draw_button(40, 425, 210, 42, "START", color(39, 174, 96))
    draw_button(40, 480, 210, 36, "RESET", color(149, 165, 166))

    fill(40)
    textAlign(LEFT, TOP)
    textSize(16)
    text("Status: " + status_msg, 310, 30)
    text("Total Weight: {:.2f} kg".format(total_weight), 310, 55)

    if len(spawn_queue) > 0:
        spawn_timer += 1
        if spawn_timer >= 25:
            spawn_timer = 0
            next_obj = spawn_queue.pop(0)
            active_trash.append(next_obj)

    for obj in active_trash[:]:
        obj.update()
        obj.display()
        if obj.landed:
            b_name = obj.get_bin()
            bin_tally[b_name] += 1
            total_weight += obj.get_weight()
            active_trash.remove(obj)
            if len(spawn_queue) == 0 and len(active_trash) == 0:
                status_msg = "Sorting complete"

    for b_name in ["Recyclable", "Organic", "General"]:
        bx = BIN_X[b_name]
        by = 440
        r, g, b = BIN_COLOR[b_name]
        fill(r, g, b)
        stroke(40)
        strokeWeight(2)
        rect(bx - 55, by - 70, 110, 130, 0, 0, 12, 12)
        fill(r - 20, g - 20, b - 20)
        rect(bx - 62, by - 82, 124, 14, 5)
        fill(255)
        textAlign(CENTER, CENTER)
        textSize(15)
        label = "Generic" if b_name == "General" else b_name
        text(label, bx, by - 35)
        textSize(28)
        text(str(bin_tally[b_name]), bx, by + 10)
        textSize(11)

def draw_button(x, y, w, h, label, bg_col):
    if x <= mouseX <= x + w and y <= mouseY <= y + h:
        fill(red(bg_col) * 0.85, green(bg_col) * 0.85, blue(bg_col) * 0.85)
    else:
        fill(bg_col)
    stroke(40)
    strokeWeight(1)
    rect(x, y, w, h, 8)
    fill(255)
    textAlign(CENTER, CENTER)
    textSize(14)
    text(label, x + w / 2.0, y + h / 2.0)

def save_to_file():
    global status_msg
    with open("trash.txt", "w") as f:
        for item in items_order:
            for _ in range(select_counts[item]):
                f.write(item + "\n")
    status_msg = "Saved to trash.txt"

def start_simulation():
    global spawn_queue, active_trash, bin_tally, total_weight, spawn_timer, status_msg
    spawn_queue = []
    active_trash = []
    bin_tally = Counter({"Recyclable": 0, "Organic": 0, "General": 0})
    total_weight = 0.0
    spawn_timer = 20

    try:
        with open("trash.txt", "r") as f:
            for line in f:
                item = line.strip()
                if not item:
                    continue
                cls = CATEGORY.get(item.lower(), GeneralTrash)
                obj = cls(item, 550, 65)
                obj.target_x = BIN_X[obj.get_bin()]
                spawn_queue.append(obj)
        if len(spawn_queue) > 0:
            status_msg = "Sorting {} items...".format(len(spawn_queue))
        else:
            status_msg = "trash.txt is empty"
    except IOError:
        status_msg = "Hit SAVE first"

def mousePressed():
    global status_msg, spawn_queue, active_trash, bin_tally, total_weight
    for i, item in enumerate(items_order):
        y_pos = 95 + i * 65
        if 140 <= mouseX <= 172 and y_pos <= mouseY <= y_pos + 32:
            if select_counts[item] > 0:
                select_counts[item] -= 1
        if 208 <= mouseX <= 240 and y_pos <= mouseY <= y_pos + 32:
            select_counts[item] += 1

    if 40 <= mouseX <= 250 and 370 <= mouseY <= 412:
        save_to_file()

    if 40 <= mouseX <= 250 and 425 <= mouseY <= 467:
        start_simulation()

    if 40 <= mouseX <= 250 and 480 <= mouseY <= 516:
        spawn_queue = []
        active_trash = []
        bin_tally = Counter({"Recyclable": 0, "Organic": 0, "General": 0})
        total_weight = 0.0
        status_msg = "Reset complete"
