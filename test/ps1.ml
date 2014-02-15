(* Fill in and submit this file *)
(* Name:  Grant Hoffecker *)
(* NetID: gfh47 *)

(** Question 3 ****************************************************************)

(**
 * [rps_round a b] accepts two symbols, [a] and [b], and determines the winner.
 * "rock" beats "scissors", "scissors" beats "paper", and "paper" beats "rock"
 * @param a b
 *     One of the choices "rock", "paper" or "scissors"
 * @return
 *     One of { -1, 0, 1, 4 }. -1 means [a] won, 1 means [b] won,
 *     0 indicates a tie.  4 indicates an invalid input.
 *)
let rps_round (a : string) (b : string) : int =
  if a = "rock" then (
    if b = "rock" then 0
    else if b = "paper" then 1
    else if b = "scissors" then -1
    else 4
  )
  else if a = "paper" then (
    if b = "rock" then -1
    else if b = "paper" then 0
    else if b = "scissors" then 1
    else 4
  )
  else if a = "scissors" then (
    if b = "rock" then 1
    else if b = "paper" then -1
    else if b = "scissors" then 0
    else 4
  )
  else 4

(* 3a *)
type move   = Rock | Paper | Scissors
type result = AWin | BWin  | Draw

(** 
 * [rps_round_enum a b] accepts two symbols, [a] and [b], and determines the
 * winner.  Rock beats Scissors, Scissors beats Paper, and Paper
 * beats Rock
 *
 * @param a b One of the choices Rock, Paper, or Scissors
 * @return One of { AWin, BWin, Draw }.
 *)
let rps_round_enum (a : move) (b : move) : result =
  if a = Rock then (
    if b = Rock then Draw
    else if b = Paper then BWin
    else AWin
  )
  else if a = Paper then (
    if b = Rock then AWin
    else if b = Paper then Draw
    else BWin
  )
  else (
    if b = Rock  then BWin
    else if b = Paper then AWin
    else Draw
  )
;;

(* 3b *)
(** 
 * [rps_round_enum a b] accepts two symbols, [a] and [b], and determines the
 * winner.  Rock beats Scissors, Scissors beats Paper, and Paper
 * beats Rock
 *
 * @param a b One of the choices Rock, Paper, or Scissors
 * @return One of { AWin, BWin, Draw }.
 *)
let rps_round_nested_match (a : move) (b : move) : result =
  match a with 
  | Rock -> (match b with 
    | Rock -> Draw
    | Paper -> BWin
    | Scissors -> AWin)
  | Paper -> (match b with
    | Rock -> AWin
    | Paper -> Draw
    | Scissors -> BWin)
  | Scissors -> (match b with
    | Rock -> BWin
    | Paper -> AWin
    | Scissors -> Draw)
;;

(* 3c *)
(** 
 * [rps_round_enum a b] accepts two symbols, [a] and [b], and determines the
 * winner.  Rock beats Scissors, Scissors beats Paper, and Paper
 * beats Rock
 *
 * @param a b One of the choices Rock, Paper, or Scissors
 * @return One of { AWin, BWin, Draw }.
 *)
let rps_round_single_match (a : move) (b : move) : result =
  match (a,b) with
  | (Rock,Scissors) -> AWin
  | (Rock,Paper) -> BWin
  | (Rock,Rock) -> Draw
  | (Scissors,Paper) -> AWin
  | (Scissors,Rock) -> BWin
  | (Scissors,Scissors) -> Draw
  | (Paper,Rock) -> AWin
  | (Paper,Scissors) -> BWin
  | (Paper,Paper) -> Draw
;;

(* 3d *)
(* accepts two moves, [a] and [b], and determines if [a] beats [b] *)
let beats (a : move) (b : move) : bool = 
  match (a,b) with
  | (Rock, Scissors) -> true
  | (Scissors,Paper) -> true
  | (Paper,Rock) -> true
  | (_,_) -> false
;;

(** 
 * [rps_round_enum a b] accepts two symbols, [a] and [b], and determines the
 * winner.  Rock beats Scissors, Scissors beats Paper, and Paper
 * beats Rock
 *
 * @param a b One of the choices Rock, Paper, or Scissors
 * @return One of { AWin, BWin, Draw }.
 *)
let rps_round_with_helper (a : move) (b : move) : result =
  if beats a b then AWin
  else if beats b a then BWin
  else Draw
;;

(** exercise 4 ****************************************************************)

(* 4a *)
(* accepts a symbol, [l], determines all pairs of elements of l *)
let all_pairs (l : 'a list) : ('a * 'a) list =
  let combined = List.map (fun ele -> (ele,l)) l in
  let pair_up = fun (ele,lst) -> List.map (fun x -> (ele,x)) lst in
  List.flatten (List.map pair_up combined)
;;

(* 4b *)

let moves = [Rock;Paper;Scissors];;

(** Takes a bool list, returns logical AND connection of all elements  *)
let (&&&) : (bool list -> bool) = List.for_all (fun x -> x);;

type rps_round_imp = move -> move -> result;;

(**  Determines if two of rps_round implementations agree on all inputs. *)
let test_rps_eq (impl1 : rps_round_imp) (impl2 : rps_round_imp) : bool = 
  (&&&) (List.map (fun (a,b) -> 
    (impl1 a b) = (impl2 a b)) (all_pairs moves));;

(* 4c *)
(** determines if all given ps_round implementations are equal on all inputs *)
let test_all_rps (impls : rps_round_imp list) : bool =
  (&&&) (List.map (fun (i1,i2) -> test_rps_eq i1 i2) (all_pairs impls));;

(** exercise 5 ****************************************************************)

type history = move list
type player  = history -> move

let always_rock : player = fun _ -> Rock

(* 5a *)

(* accepts two moves, and determines if [b] beats [a] *)
let loses (a:move) (b:move) : bool = beats b a;;

(* Player plats to beat most recent opponent move, plays Rock on 1st move *)
let beats_last : player = function
  | [] -> Rock
  | hd::tl -> (match hd with
    | Rock -> Paper
    | Paper -> Scissors
    | Scissors -> Rock)
;;

(* Player plats to beat most recent opponent move, plays Rock on 1st move 
 * 
 * this is an alternative, potentially more unsafe application
 *) 
let beats_last_alt : player = function
  | [] -> Rock
  | hd::tl -> try List.find (loses hd) moves with _ -> Rock
;;

(* 5b *)

(** Returns a player that always plays the given move *)
let always_plays (what : move) : player = fun _ -> what;;

(* 5c *)

(* Determines if p1 beats p2 after playing until one of them wins *)
let rps_game (p1 : player) (p2 : player) : bool =
  let rec rps_game_handler (h1 : history) (h2 : history) : bool = 
    let (m1,m2) = (p1 h2),(p2 h1) in 
    match rps_round_with_helper m1 m2 with
    | AWin -> true
    | BWin -> false
    | Draw -> rps_game_handler (m1::h1) (m2::h2) in
  rps_game_handler [] []
;;

(** exercise 6 ****************************************************************)

(* 6a *)

(** Breaks given list into adjacent pairs, applies a function to each pair.
 * It returns a list containing the resulting values.
 * 
 * @param compare a function that returns one of two values
 * @param lst a list of values resulting from the comparisons. 
 *)
let pair_filter (compare : 'a -> 'a -> 'a) (lst : 'a list) : 'a list =
  let rec pf_helper (l : 'a list) : 'a list = 
    match l with 
    | [] -> []
    | [last] -> [last]
    | hd::sd::tl -> (compare hd sd)::(pf_helper tl) in
  pf_helper lst
;;

(* 6b *)

(** Repeatedly breaks given list into adjacent pairs, applies a function 
 * to each pair, and continues till one value remains.
 * 
 * @param compare a function that returns one of two values
 * @param lst a list of values resulting the comparison driven shrinking
 *)
let tournament (compare: 'a -> 'a -> 'a) (lst : 'a list) : 'a option =
  let rec t_helper (l : 'a list) : 'a option = 
    match l with
    | [] -> None
    | [w] -> Some w
    | hd::sd::tl -> t_helper (pair_filter compare l) in
  t_helper lst
;;

(** optional karma ************************************************************)

(* Returns a random element within a list *)
let random_element (lst:'a list) : 'a option =
  match lst with
  | [] -> None
  | _ -> Some (List.nth lst (Random.int (List.length lst)))
;;

(* Returns a player that plays a random move *)
let random_player : player = fun history -> 
  match random_element moves with
  | None -> Rock 
  | Some x -> x
;;

let string_of_move (m:move) : string = match m with
  | Rock -> "rock"
  | Paper -> "paper"
  | Scissors -> "scissors"
;;

(** Takes two players and keeps running rounds until one of them wins
 * or a fixed number of runs occur, which then a Draw would occur.  
 * Determines if player 1 beats player 2.
 *
 * @param p1 p2 players, k number of rounds to play until forced draw
 * @return result, if p1 beat p2
 *)
let rps_game_limited (p1 : player) (p2 : player) (k:int) : bool =
  let rec rps_game_handler (h1 : history) (h2 : history) (c : int) : bool = 
    if c < k then 
      let (m1,m2) = (p1 h2),(p2 h1) in 
      let (m1_str,m2_str) = (string_of_move m1),(string_of_move m2) in
      Printf.printf "Round %i: p1:%s p2:%s\n" c m1_str m2_str; 
      match rps_round_with_helper m1 m2 with
      | AWin -> true
      | BWin -> false
      | Draw -> rps_game_handler (m1::h1) (m2::h2) (c+1)
    else
      false 
    in
  rps_game_handler [] [] 0
;;

(** Takes two players and keeps running rounds until one of them wins
 * k rounds, Determines if player 1 beats player 2.
 *
 * @param p1 p2 players, k number of rounds to win to win overall
 * @return result, if p1 beat p2
 *)
let rps_game_best_of (p1 : player) (p2 : player) (k:int) : bool =
  let rec mast (h1:history) (h2:history) (c:int) (s1:int) (s2:int) : bool = 
    if s1 >= k then true
    else if s2 >= k then false
    else (
      let (m1,m2) = (p1 h2),(p2 h1) in 
      let (m1_str,m2_str) = (string_of_move m1),(string_of_move m2) in
      Printf.printf "Current Score: p1:%i p2:%i\n" s1 s2; 
      Printf.printf "Round %i: p1:%s p2:%s\n" c m1_str m2_str; 
      match rps_round_with_helper m1 m2 with
      | AWin -> mast (m1::h1) (m2::h2) (c+1) (s1+1) s2 
      | BWin -> mast (m1::h1) (m2::h2) (c+1) s1 (s2+1) 
      | Draw -> mast (m1::h1) (m2::h2) (c+1) s1 s2 
    ) in
  Printf.printf "Game, best %i of %i\n" k (2*k-1); 
  mast [] [] 0 0 0
;;

(** Takes a list of (player,player name) tuples, runs a tournament of 
 * adjacent players, returns the name of the winner of the tournament
 * If given empty list, returns "No Winner"
 *)
let rps_tourney (l:(player*string) list) : string = 
  let compare (p1:player*string) (p2:player*string) : player*string =
    if rps_game (fst(p1)) (fst(p2)) then p1
    else p2 in
  match tournament compare l with 
  | None -> "No winner"
  | Some (p,str) -> str
;;
