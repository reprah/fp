; Week 3

(require '[clojure.string :as str])

(def lines-vector
  [1 5 -2 3 2 5 4 -7 2 -3])

(defn median [vector]
  (let [sorted (vec (sort (filter pos? vector)))
        vec-length (count vector)
        middle-index (if (odd? vec-length)
                       (- (Math/round (/ vec-length 2.0)) 1)
                       (- (/ vec-length 2) 1))]
    (get sorted middle-index)))

; Algorithm:
;
; Things to keep track of: states, the next lines, and the current iteration
; States are the values we're calculating the median with
; states: { 1 => [1], 2 => [1 5] } etc.

; Base case: if there are no more lines to read, return
; Recursive case:
;  - set previous state to the state during the last iteration, or an empty
;    vector if there was none
;  if we're rolling back (the current line is a negative num)
;    - calculate the state we want to rollback to and fetch it from the states map/dictionary
;    - set the state for this iteration to the rolled-back state
;    - print the median of this current state
;    - recurse w/ new values
;  if we're not rolling back,
;    - add the current number to the previous set of numbers
;    - calculate the median of that
;    - recurse w/ new values

(defn messy-median [states, lines, iteration]
  (if (empty? lines)
    nil
    (let [previous-state (if (empty? states) [] (states (- iteration 1)))
          current-line (first lines)
          new-lines (rest lines)]
      (if (> 0 current-line)
        (let [rollback-to (+ iteration current-line)
              current-state (states rollback-to)
              new-states (assoc states iteration current-state)]
          (println (median current-state))
          (messy-median new-states new-lines (+ 1 iteration)))
        (let [current-state (conj previous-state current-line)
              new-states (assoc states iteration current-state)]
          (println (median current-state))
          (messy-median new-states new-lines (+ 1 iteration)))))))

(messy-median {} lines-vector 0)  
