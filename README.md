# minesweeper

**Create a Game**
----

* **URL**

  /game/

* **Method:**

  `POST`
  
*  **URL Params**

   **Optional:**

   `rows=[integer]`
   `columns=[integer]`
   `mines=[integer]`

* **Success Response:**

  * **Code:** 201 <br />
    **Content:** `{ id : 12 }`

* **Error Response:**

  * **Code:** 401 UNAUTHORIZED (Not implemented yet) <br />
    **Content:** `{ error : "You are unauthorized to make this request." }`

**Place a dot**
----

* **URL**

  /game/<id>/play

* **Method:**

  `POST`
  
*  **URL Params**

   **Required:**

   `x=[integer]`
   `y=[integer]`

   **Optional:**
   `flag=[boolean]`

* **Success Response:**

  * **Code:** 201 <br />
    **Content:** `{ dots : [0;0 : 2, 0;2 : 1, 1;3 : 1, 1;2 : f], status: "STARTED" }`


* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ error : "Dot outside of boundaries" }`

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{ x: ["This field is required." ], y: ["This field is required." ]}`

  * **Code:** 403 BAD REQUEST <br />
    **Content:** `{ error : "Game already finished" }`

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ error : "Invalid game id" }`
