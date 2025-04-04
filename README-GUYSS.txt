>>>> FOR IMPORTING DATABASE <<<<

use re_Estate;
source  D:\comp_project\Dump20250327.sql



>>>> FOR COPYING THE CODE FILE <<<<

simply copy and paste the entire "code" folder. it contains the latest images in "images" folder and the latest code in the file called "main_tk.py"



>>>> WHAT YOU HAVE TO DO <<<<

1. Creating GUI for prop_det_frame()

define a function named prop_det_open() like this -> def prop_det_open():
under this create the gui for prop-det-frame, refer prop-det.png
(ik irene was working on it but i was bored so hehhheheh, also if u wanna edit the gui and make some changes go ahead w it 👍)
go to the ENDD of the code and there will be a ">>> PROP DETAIL FRAME FUNCTIONS <<<<" define it there. 
ex:
def prop_det_open():
	<the code for gui only>

2. if you wish to do FUNCTIONS:

define a function where you generate the property_id code. the gui for the post-prop-frame is under a function called post_prop_open().
simply define a function UNDER this function and name it prop_id_gen() like this -> def prop_id_gen():
under this function, use ur brain and RETURN a STRING that will be the prop id. you can access all the necessary info using the variables and stuff defined in the gui by irene :>. (again, the gui is under a function called post_prop_open)
ex:
def post_prop_open():

	<the gui code>				# the gui code irene coded

	def post_prop():			# a function im working on to add new prop to database
		<sm code im working on>

	def prop_id_gen():			#the function you define to generate the prop-id
		<ur code>
		return <the final string>

this is the format of the prop_id: <sell/lease: S/L> <prop-cat: RI/RV/RA/C/P> <state: ex: KA/KL/etc> <a serial number: ex: 0004>

ex: if the user selected SELL and prop-cat as APARTMENT and location as Chennai (which is in TamilNadu) then the prop-id will be: "SRATN0004"

places where you might (or definitely will) get stuck are: accessing the state selected because user doesn't select any state in post-prop, they only select city. and adding that number at the end which a serial number in the database. well, figure it out :)

3. 

