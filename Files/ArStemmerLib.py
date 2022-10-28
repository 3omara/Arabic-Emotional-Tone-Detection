# -*- coding: utf-8 -*-
# Author Samhaa R. El-Beltagy
# Version 1.1


class ArStemmer:

    def __init__(self, stpWdsFile="Files\\arabicStops.txt"):
        self.stopWords = set([])
        self.stpWdsFile = stpWdsFile
        self.dict = set([])
        self.stemDict = {}
        self.unique = set([])
        self.irreg = {}
        self.loadSet(stpWdsFile, self.stopWords)
        self.loadDict("Files\\irreg.txt")
        self.removeTeh = False
        self.enforceStemming = False

    def loadSet(self, fname, setToLoad):
        f = open(fname, 'r', encoding='utf8')
        for line in f:
            line = line.strip()
            line = self.replaceChars(line)
            setToLoad.add(line)
        f.close()

    def replaceChars(self, word):
        if len(word) < 1:
            return word

        if (word[0] == '\uFEFF'):
            word = word[1:]
        t = word.find("\uFEFB")
        if t >= 0:
            word = word[0:t] + u"لا" + word[t + 1:]
        if word.endswith(u"ى"):
            word = word[0: len(word) - 1] + u"ي"
        word = word.replace(u'أ', u'ا')
        word = word.replace(u'إ', u'ا')
        word = word.replace(u'آ', u'ا')
        word = word.replace(u'ة', u'ه')
        if word.endswith(u"اً"):
            word = word[0: len(word) - 2] + u"ا"

        return word

    def loadDict(self, fname):
        f = open(fname, 'r', encoding='utf8')
        i = 1
        for s in f:
            par = s.split()
            if len(par) != 2:
                print("Error reading " + fname, i, len(par))
                i = i+1
                continue
            entry = par[0]
            stem = par[1]
            entry = self.replaceChars(entry)
            stem = self.replaceChars(stem)
            self.irreg[entry] = stem
            i = i+1
        f.close()

    def loadDicts(self, dictFiles):
        for f in dictFiles:
            self.loadSet(f, self.dict)

    def checkInDicts(self, word, stem):
        if stem in self.dict:
            return [word, stem, True, True]
        if stem in self.stopWords:
            return [word, stem, False, True]
        return [word, stem, False, False]

    def sepLah(self, w):
        if w.startswith(u"لا"):
            t = w[2:]
            r = self.checkInDicts(w, t)
            if r[3]:
                return r
            t = w[1:]
            r = self.checkInDicts(w, t)
            if r[3]:
                return r

    def removePre(self, w):
        if len(w) < 4:
            return w

        pres = [u"و", u"ال", u"وال", u"بال", u"كال", u"فال",
                u"لل", u"وبال", u"ولل", u"وكال", u"وفال"]
        possible = w
        for pre in pres:
            l = len(pre)
            if w.startswith(pre) and (len(w) - l) > 1:
                t = w[len(pre):]
                r = self.checkInDicts(w, t)
                if r[3]:
                    return r
                if l > 1:
                    possible = t
        if(possible == w):
            return [w, w, False, False]
        return [w, possible, False, True]

    def removePost(self,  r):
        rec = [r[0], r[1], r[2], r[3]]
        if len(rec[1]) < 3:
            rec[3] = False
            return rec
        word = rec[1]
        if word in self.irreg:
            rec[1] = self.irreg[word]
            rec[2] = rec[3] = True
            return rec

        result = word
        posts = [u"ها", u"وا", u"كم", u"نا", u"هم", u"هن", u"ان",
                 u"هما", u"ين", u"ون", u"ه", u"ات", u"ي", u"يه"]
        if len(word) > 2:
            for post in posts:
                if result.endswith(post) and len(result) > 2:
                    result = result[0: len(result) - len(post)]
                    if len(result) < 2:
                        return rec

                    if result == u"ال" or result == u"لل":
                        return rec

                    if post == u"ات":
                        f2 = ""
                        if result.endswith(u"ه"):
                            f2 = result[0: len(result)-1]
                        else:
                            f2 = result + u"ه"
                        if f2 in self.dict:
                            rec[1] = f2
                            rec[2] = rec[3] = True
                            return rec

                    if result in self.dict or result in self.stopWords:
                        rec[1] = result
                        rec[2] = rec[3] = True
                        return rec

                    if result in self.irreg:
                        rec[1] = self.irreg[result]
                        rec[2] = rec[3] = True
                        return rec

                    if result.endswith(u"ت") and len(result) > 2:
                        res2 = result[0:len(result)-1] + u'ه'
                        if res2 in self.dict or res2 in self.stopWords:
                            rec[1] = res2
                            rec[2] = rec[3] = True
                            return rec

                    f2 = result + u"ه"
                    if f2 in self.dict:
                        rec[1] = f2
                        rec[2] = rec[3] = True
                        return rec

                if rec[2]:
                    return rec

            post = u"ا"
            if result.endswith(post) and len(result) > 2:
                res2 = result[0: len(result)-len(post)]
                if res2 in self.dict or res2 in self.stopWords:
                    rec[1] = res2
                    rec[2] = rec[3] = True
                    return rec

            post = u"ك"
            if result.endswith(post) and len(result) > 3:
                res2 = result[0: len(result)-len(post)]
                if res2 in self.dict or res2 in self.stopWords:
                    rec[1] = res2
                    rec[2] = rec[3] = True
                    return rec

            rec[1] = result
            return rec

    def removeExtraChar(self, pre, s):
        if len(s) - len(pre) < 2:
            return [s, s, False, False]
        if(s.startswith(pre)):
            t = s[len(pre):]
            if t in self.dict:
                return [s, t, True, True]
            elif t in self.stopWords:
                return [s, t, False, True]
            else:
                temp = self.removePost([t, t, False, False])
                t = temp[1]
                if t in self.dict:
                    return [s, t, True, True]
                elif t in self.stopWords:
                    return [s, t, False, True]

        return [s, s, False, False]

    def removeExtraCharList(self, charList, rec):
        for ch in charList:
            r = self.removeExtraChar(ch, rec[1])
            if r[3]:
                return r
        return rec

    def removeTeh(self, s):
        if len(s) < 3:
            return s
        p1 = u"ة"
        p2 = u"ه"
        if s.endswith(p1) or s.endswith(p2):
            s = s[0: len(s)-1]
        return s

    def forceStemming(self, s):
        if len(s) < 3:
            return s
        if s.startswith(u"و") and (not s in self.dict):
            s = s[1:]
        if len(s) < 3:
            return s
        if s.endswith(u"ي"):
            s = s[0: len(s)-1]
        else:
            s = self.removeTeh(s)
        return s

    def removeWaw(self, s):
        if len(s) < 4:
            return s
        pre = u"و"
        if s.startswith(pre):
            return s[1:]
        return s

    def stem(self, s):
        if len(s) < 3:
            return s
        s = s.strip()
        s = self.replaceChars(s)
        if s in self.dict or s in self.stopWords:
            return s
        if s in self.irreg:
            return self.irreg[s]
        mod = self.removePre(s)
        if mod[2]:
            return mod[1]
        mod2 = self.removePost(mod)
        if mod2[2]:
            return mod2[1]
        if not mod[2]:
            r = self.removeExtraCharList([u"و", u"ف", u"ب", u"ل", u"ك"], mod)
            # print(r,"ll")
            if r[3]:
                return r[1]
            f = u"يا"
            r = self.removeExtraChar(f, mod[1])
            if (r[3]):
                r[1] = f + u" " + r[1]
                return r[1]
           # f= u"لا"
            #r = self.removeExtraChar(f, mod[1])
            # if (r[3]):
              #  r[1] = f + " "+ r[1]
              #  return r[1]  '''

        r2 = self.removeExtraCharList([u"و", u"ف", u"ب", u"ل", u"ك"], mod2)
        # print(r2,"9")
        if r2[3]:
            return r2[1]
        r = self.removePost(r)
        if r[3]:
            return r
        r[1] = self.removeWaw(r[1])
        if self.enforceStemming:
            return self.forceStemming(r[1])
        elif self.removeTeh:
            return self.removeTeh(r[1])

        return r[1]
