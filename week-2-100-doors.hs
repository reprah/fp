doors = [1..100]


countDoorsOpen :: [Int] -> Int
countDoorsOpen doorIndices = (sum . map isOpen) doorIndices


isOpen :: Int -> Int  -- returns 1 for open, 0 for closed
isOpen n = mod nVisits 2  -- door left open if 'visited' an odd number of times
    where nVisits = (sum . mapDivisibilityTest) [1..n]
          mapDivisibilityTest = map (\n2 -> if mod n n2 == 0 then 1 else 0)
          -- an integer n2 'visits' n if and only if n2 divides n


test = 10 == (countDoorsOpen doors)
