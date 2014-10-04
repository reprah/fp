; 100 Doors

(def doors (map (fn [_] :closed) (range 1 101)))

(defn toggle-door [door]
  (if (= door :open) :closed :open))

(defn divisible? [index current-pass]
  (= 0 (mod index current-pass)))

(defn hundred-doors [doors current-pass]
  (if (= 100 current-pass)
    doors
    (recur
      (map-indexed
        (fn [index, door]
          (if (divisible? index current-pass) (toggle-door door) door))
        doors)
      (+ 1 current-pass))))

(hundred-doors doors 1)
