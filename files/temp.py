import wave, struct, math, random
from perlin_noise import PerlinNoise
noise = PerlinNoise()

# Ajout possible de {#STARTDATA"} pour noise etc 

sampleRate = 44100 # hertz

obj = wave.open('out.wav','wb')

obj.setnchannels(1)
obj.setsampwidth(2)
obj.setframerate(sampleRate)


def ins_0(i,frequency):
  freq = frequency
  return math.sin(frequency*math.pi*2*i)
def ins_1(i,frequency):
  freq = frequency
  t = i*frequency % 1
  out = 1
  i2 = ((i/2)**1.5)/4
  if 0.5-i2 <= t <= 0.5+i2:out *= -1
  if t >=0.5: out *=-1
  return out
def ins_2(i,frequency):
  freq = frequency
  return noise(i*freq)



notes = [(880,0,10,ins_2,1)]
# 32767

max_len = max([x[2]+x[1] for x in notes])
if max_len > 60: max_len = 60

out = [0 for x in range(max_len*sampleRate)]

for i,(freq,start,duration,ins,volume) in enumerate(notes):
    print("Doing note:",i)
    for x in range(duration*sampleRate):
        out[start*sampleRate+x] += ins(x/sampleRate,freq)*volume

print("out = ", out[0:100])
print("Writing frames...")

for i in out:
    if i >= 1: i = 1
    elif i <= -1: i = -1
    obj.writeframesraw( struct.pack('<h',int(i*32767)) )
obj.close()