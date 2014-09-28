; Week 1, Super Digit

(require '[clojure.string :as str])

(defn calculate-p [n k]
  (let [n-range (range 0 n)]
    ; read-string tries to extract an object from a string,
    ; couldn't use Integer/parseInt because the numbers were too large
    (read-string (apply str (map (fn [_] (str k)) n-range)))))

(defn integer-list [digit]
 ; get the individual integers by turning the number into
 ; a string, splitting it on '', and map them to integers
 (map read-string (rest (str/split (str digit) #""))))

(defn super-digit [digit] 
  ; if the length of the digit when turned into a string is 1,
  ; return that number
  (if (= (count (str digit)) 1)
    digit
    ; else, get the sum of each digit in the number
    ; and recurse with the sum as the new argument
    (super-digit (reduce + (integer-list digit)))))

(defn super-digit-main [input]
  (let [[n, k] (map read-string(str/split input #" "))]
    (super-digit (calculate-p n k))))

(println (super-digit-main "148 3"))
