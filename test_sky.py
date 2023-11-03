import sky

sky = sky.Skywatcher((40.11083232724192, 88.22444223575499))

light_times = sky.get_dark_times()

for t in light_times: print(t)



