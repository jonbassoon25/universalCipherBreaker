import json

new = {}
old = {}

with open("./jsonMergerFiles/new.json") as newFile:
    new = json.load(newFile)

with open("./jsonMergerFiles/old.json") as oldFile:
    old = json.load(oldFile)

for key in new.keys():
    if key in old.keys():
        for subkey in new[key].keys():
            if subkey in old[key].keys():
                for value in new[key][subkey]:
                    old[key][subkey].append(value)
            else:
                print(f"Adding: {key}/{subkey}")
                old[key][subkey] = new[key][subkey]
    else:
        print(f"Adding: {key}/*")
        old[key] = new[key]

#sort subkeys
result = {}
for key in old.keys():
    result[key] = {}
    for subkey in [str(num2) for num2 in sorted([int(num) for num in list(old[key].keys())])]:
        result[key][subkey] = old[key][subkey]

with open("./jsonMergerFiles/result.json", "w") as resultFile:
    json.dump(result, resultFile)