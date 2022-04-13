Nume: Prioteasa Cristi Andrei
Grupă: 332 CC 

# Tema 1

Organizare
-
1. Explicație pentru soluția aleasă:

   Am folosit lock-uri pentru metodele : place_order,remove_from_cart,add_to_cart,publish,register_producer.
   Marketul tine un dictionar pt produse de forma <producer_id,(produs,id_celui_care_a_rezervat_produsul)> default id_celui_care_a_rezervat_produsul va fi -77, insemnand ca produsul nu a fost rezervat de niciun consumer si nu se afla in niciun cos.
   Marketul tine un dictionar pt basketuri de forma <cart_id,[(produs,id_producator)]>. Tin tuplu cu un id_producator sa stiu in caz ca vreau sa returnez produsul inainte de a fi cumparat in ce lista il voi gasi. A rezerva un produs inseamna a il adauga in cos si a ii schimba id_celui_care_a_rezervat_produsul din -77 in id_cos consumer.

   La o publicare de produs se adauga in lista corespunzatoare acelui producer , deja inregistrat  cu (produs,-77).
   Cand un consumer face un add_to_cart acel produs va fi cautat si va deveni rezervat ca (produs,id_cos_consumer) si va ramane in lista acelui producator, va fi scos doar la place_order

   remove_from_cart gaseste produsul si il face iar de forma (produs,-77) adica disponibil pentru alti consumeri.

   Am implementat logging, nu si unittesting.

* De făcut referință la abordarea generală menționată în paragraful de mai sus. Aici se pot băga bucăți de cod/funcții - etc.
* Consideri că tema este utilă?
* Consideri implementarea naivă, eficientă, se putea mai bine?

***Opțional:***


* De menționat cazuri speciale, nespecificate în enunț și cum au fost tratate.


Implementare
-

* De specificat dacă întregul enunț al temei e implementat
* Dacă există funcționalități extra, pe lângă cele din enunț - descriere succintă + motivarea lor
* De specificat funcționalitățile lipsă din enunț (dacă există) și menționat dacă testele reflectă sau nu acest lucru
* Dificultăți întâmpinate
* Lucruri interesante descoperite pe parcurs


Resurse utilizate

Laburi asc, documentatie python , gfg 

Git
-
1. Link către repo-ul de git

Repo-ul e privat, ask for read permission 

https://github.com/PrioteasaAndrei/tema-asc-1.git
