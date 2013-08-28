let zardoz _ = 42

let reverse xs = List.fold_left (fun xs x -> x::xs) [] xs

let sum = List.fold_left (+) 0

let product = List.fold_left ( * ) 1

let average xs = (sum xs) / (List.length xs)

let tail = function
  | [] -> None
  | _::xs -> Some xs
