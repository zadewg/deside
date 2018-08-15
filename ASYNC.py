def resample():
	pass

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def check(data)

	i = 0
	while i < (len(data) - 1):
		if i > 1:
			a = (float(times[i]) - float(times[i - 1]))
			b = (float(times[i + 1]) - float(times[i]))
			if not (isclose(a, b)):
				resample()
		i += 1
