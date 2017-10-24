import re
import unicodedata
s = "jackie chutiya\ud83d\ude02\ud83d\ude02\ufeff"
print ''.join([i if ord(i) < 128 else ' ' for i in s])
text_new = s.decode('ascii', 'ignore')
print text_new

start = s.find("\u")
end = len(s)
s = s[:start]
print s
