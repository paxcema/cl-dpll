;;;; Patricio Cerda Mardini. July 2015 v1, February 2016 v2.
;;;;
;;;; This is a simple 3-SAT solver, 'translated' from Python to CL, for learning purposes.
;;;; It applies the Tautology, Unit Clause, Pure Literal, and Ordinary Bifurcation rules.

;;;; Input functions.
;;;; Note: On the Python version, just parsing instanciaS3U.txt takes between 1.03 - 1.51 seconds,
;;;; whereas on Lisp it takes 0.003 seconds!

(defun read-instance (path)
  "Reads the SAT instance from a .txt, saving it on a list."
  (let ((instance '()))
    (with-open-file (file ; Stream name
		     path ; To the file
		     :direction :input) ; Declaring it as an input
      (do ((line (read-line file nil 'eof)
  	         (read-line file nil 'eof)))
	  ((eql line 'eof))
	(setf instance (append instance (list (cleaner (parse-line line)))))))
    instance))

(defun parse-line (line &key (start 0) (acc nil))
  "Processes a number-separated-by-spaces string, returning a list by using parse-integer"
  (if (not acc)
      (multiple-value-bind
            (acc new-start)
          (parse-integer line :start start :junk-allowed t)
        (parse-line line :start new-start :acc (list acc)))
      (multiple-value-bind
            (acc2 new-start)
          (parse-integer line :start start :junk-allowed t)
	(if (= new-start (length line))
	    (append acc (list acc2))
	    (parse-line line :start new-start :acc (append acc (list acc2)))))))

(defun cleaner (lst)
  "Aux. function, cleans up the NIL remnant from (parse-line)"
  (dolist (item lst)
    (if (not item)
	(setf lst (remove item lst))))
  lst)

;;;; Logic functions
;;;; Note: in solving a small (but not tiny) instance, Lisp takes approximately 0.03 seconds.
;;;; Python takes more than half an hour (and a lot of battery)... didn't stick for it to
;;;; finish, though.

;;;; Benchmark (for 20 atoms, 91 clausules):
;;;; B1-10: Python 0.22 s, Lisp 0.01 s
;;;; B1-200: Python 0.38 s, Lisp 0.01 s
;;;; B1-1000: Python 0.57 s, Lisp 0.02 s

(defun simplificacion (alpha lit)
  "Simplifies an expression, given that one literal is true"
  (let ((beta nil))
    (dolist (sublist alpha)
      (if (and (not (member lit sublist)) (not (member (* -1 lit) sublist)))
	  (if beta ; Both element and inverse are not present. Clausule is added to beta as is.
	      (setf beta (append beta (list sublist)))
	      (setf beta (list sublist)))
	  (if (member (* -1 lit) sublist) ; Inverse present, clausule added without that atom.
	      (if beta ; If the element is there, we add nothing.
		  (setf beta (append beta (list (delete (* -1 lit) sublist))))
		  (setf beta (list (delete (* -1 lit) sublist)))))))
    (if (> (length beta) 1)
	(cleaner beta)
	beta)))	

;;;; Falta hacer que retorne el valor de la rama que dio el resultado, USANDO CATCH & THROW!!
(defun DPLL (alpha recorrido &optional (deep 0))
  "Base DPLL function. If true, returns T and prints the necessary truth value. NIL otherwise."
  (if (not alpha) ; Base case for T.
      (progn
	; (setf *3sat-soln* recorrido) ; Use as temporary return
	(format t "SOLUTION FOUND. Let ~A all be true (~A levels deep) for it.~%" recorrido deep)
	t)
      (if (equal '(nil) alpha)
	  nil ; Base case for F.
	  (let* ((i 0) ; Else case. Note the use of let*, to use i and j on the lit definition.
		 (j 0)
	         (lit (nth j (nth i alpha)))) ; For each element in each sublist of alpha.
	    (loop until (not (member (abs lit) recorrido)) do ; A (do) would be more lispy...
		 (if (nth (+ 1 j) (nth i alpha))
		     (setf lit (nth (+ 1 j) (nth i alpha)))
		     (setf lit (nth 0 (nth (+ i 1) alpha))))) ; Finds next literal not on the path
	    (if (not recorrido)
		(setf recorrido (list lit))
		(setf recorrido (append (list lit) recorrido))) ; We add it to the path
	    (if (DPLL (simplificacion alpha lit) recorrido (1+ deep))
		t ; And check for a solution using it.
		(progn ; When it doesn't work, we try using the inverse.
		  (if (not recorrido)
		      (setf recorrido (list (* lit -1)))
		      (setf recorrido (cons (* lit -1) (cdr recorrido))))
		  (DPLL (simplificacion alpha (car recorrido)) recorrido (1+ deep))))))))

;;;; Output functions

(defun main-repl ()
  "Simple (timed) loop, for benchmarking reference. Enters a break-loop if invalid path is given"
  (format t
	  "Bienvenido al 3SAT solver implementado 
           en Common Lisp! ingresa un path (absoluto 
           o relativo) del archivo .txt a evaluar!")
  (let ((path (string (read-line)))) 
;    (progn
;      (unwind-protect
;	   nil
;	   (with-open-file (testfile path :direction :input))
	(time (DPLL (read-instance path) nil))
	(main-repl)))
