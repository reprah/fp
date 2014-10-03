superDigit :: Int -> Int
superDigit n = _superDigit (asString n)

_superDigit :: String -> Int
_superDigit (digit:[]) = asInt digit
_superDigit digits = _superDigit (asString digitSum)
    where digitSum = sum (map asInt digits)

asString = show

asInt :: Char -> Int
asInt n = read [n] :: Int
-- convert Char to String (i.e., [n]) and then String to Int
