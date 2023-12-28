

currentFrame = 0
animationCounter = 0
animationDuration = 150

for i in range(1000):
    print(currentFrame)
    if animationCounter < animationDuration:
        animationCounter += 1
    else: 
        animationCounter = 0
    currentFrame = int(animationCounter/(animationDuration/13))
            