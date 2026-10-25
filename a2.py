from collections import Counter


class Trash:

  def __init__(self, name):
    self.name = name

class RecyclableTrash(Trash):
  def get_bin(self):
    return "Recyclable"

class OrganicTrash(Trash):
  def get_bin(self):
    return "Organic"


class GeneralTrash(Trash):
  def get_bin(self):
    return "General"


CATEGORY = {
    "plastic": RecyclableTrash,
    "paper": RecyclableTrash,
    "food": OrganicTrash,
    "wrapper": GeneralTrash,
}

t = Counter()

with open("trash.txt", "r") as f:
  for line in f:
    item = line.strip()
    if not item:
      continue

    cls = CATEGORY.get(item.lower(), GeneralTrash)
    obj = cls(item)

    bin_name = obj.get_bin()
    t[bin_name] += 1
    print(f"{obj.name} = {bin_name}")

print("--- Trash Count ---")
for bin_name, count in t.items():
  print(f"{bin_name}: {count}")