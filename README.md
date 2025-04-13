# Real-Estate
*NOTE:* Do not directly edit the main_tk file instead send the code snippets to owner via Gmail. All data added to your local MySQL databases will not be reflected in the repository unless data has been imported to owner's database. For that contact owner.

*SUGGESTION:* Create a new folder in your local pc and copy all files of Real-Estate in the folder and edit. Don't forget to import the MySQL data in your local database.

> # THE CODE STRUCTURE:
Real Estate Management App
├── Main Window Setup
│   ├── Theme, Size, Title
│   └── MySQL Connection

├── Frame Definitions
│   ├── login_frame
│   ├── main_frame
│   ├── profile_frame
│   ├── prop_detail_frame
│   └── post_prop_frame

├── Login Frame
│   ├── Common Login Functions
│   ├── Sign In
│   ├── Sign Up
│   ├── Forgot Password
│   ├── Email Validation
│   └── Login Frame UI

├── Main Frame
│   ├── UI Layout
│   ├── Sidebar & Navigation
│   ├── Property Search
│   │   ├── Suggest Locations
│   │   └── Entry Fill
│   ├── Property Display
│   │   └── create_property_frame()
│   └── Search Frame UI

├── Profile Frame
│   ├── Logout
│   ├── Edit Profile
│   │   ├── Change Image
│   │   ├── Edit Fields
│   │   ├── Reset Password
│   │   └── Delete Account
│   └── Profile Frame UI

├── Post Property Frame
│   ├── Open & Navigate
│   ├── Post Form Sections
│   │   ├── Sell/Lease
│   │   ├── Property Type
│   │   ├── Property Details
│   │   ├── Media Upload
│   │   ├── Pricing Details
│   │   └── Co-living Option
│   ├── Validate Form
│   ├── Upload Images
│   └── Submit to Database

└── Property Detail Frame
    ├── Open & Navigate
    ├── Property Information Display
    ├── Description Section
    ├── Images Section
    └── Owner Contact Info



> # FEATURES ADDED:
1. a sign up page with working sign in and forgot password
3. a profile page that displays minimum user data and option to log out
0. displays role in profile page
1. changing profile photo -> integrate w database

> # FEATURES TO ADD:
2. password reset option in profile page
4. sidebar that contains buttons according to user role
3. a home page that displays a search bar (working) and trending properties/ newly added properties

> ### To Import the MySQL Data
use re_estate;
source <File\\Path\\with\\double\\slashes>\\<DumpFileName.sql>;
ex:
use re_estate;
source D:\\comp_project\\code\\DumpFileName.sql;

> # PROMPTS
### **🏡 Profile Page Contents**

**1️⃣ Common Sections (For All Users)**
- **Profile Picture** (Editable)  
- **Full Name**  
- **Email Address**  
- **Phone Number**  
- **Role** (Owner, Tenant, Agent)  
- **Password Reset Option**  

 **2️⃣ For Property Owners**
- **Listed Properties** (Grid/List View with images, price, status)  
- **Earnings Dashboard** (Rental income, pending payments, analytics)  
- **Tenant Requests** (Maintenance requests, inquiries)  
- **Add New Property** (Button to add new listings)  
- **Property Performance Reports** (Occupancy rate, rental trends)  

 **3️⃣ For Tenants**
- **Rented Property Details** (Address, rent amount, lease duration)  
- **Rent Payment Status** (Paid, Due, Overdue)  
- **Maintenance Requests** (Raise & track service requests)  
- **Lease Documents** (Access signed lease agreements)  
- **Payment History** (List of past payments)  

 **4️⃣ For Real Estate Agents**
- **Managed Properties** (Properties assigned to them)  
- **Client Inquiries** (New leads, interested buyers/renters)  
- **Upcoming Appointments** (Schedule with clients)  
- **Commission Dashboard** (Earned commissions, pending payments)  
- **Documents & Agreements** (Upload property papers, contracts)

> # THE BASIC BLUEPRINT
# **Blueprint for Real Estate Management App**

## **User Flow**
1. **User Opens App**
   - *Extra Feature:* Auctions by Banks

2. **Login Page**
   - Existing Users: Login with User ID & Password
   - New Users: Create an Account (Name, Email ID, Phone Number)
   - Forgot Password Option

3. **Profile Setup Page**
   - Name
   - Email ID
   - Phone Number

---

## **Main Features & Pages**

### **1. Update Profile Page**
- Users can edit Name, Email ID, and Phone Number

### **2. Home Page**
- Displays user information:
  - Name
  - Email ID
  - Phone Number
  - User ID
  - Contacted Properties

### **3. Post Your Property**
- Users can list properties with the following details:
  - Address (Street, City, State)
  - Area (sqft)
  - Number of Rooms
  - Floor
  - Rent/Sale Price
  - Deposit (if applicable)
  - Contact Number
  - Email
  - Photos
  - Date of Posting

### **4. Search Properties**
- **Search by Location** (City, State, *Bengaluru only*)
  
  #### **(a) Buying/Renting**
  - Buy a House
  - Rent a House
  - Rent a Commercial Plot
  - Rent a Commercial Room
  - Buy a Plot
  
  #### **(b) Co-Living/PG/Hostel**
  - Rent a PG
  - Hostel for Kids (Under 18) *(Includes Guardian Details)*

### **5. Property Categories**

#### **Selling**
- Put up House for Lease (Rent)
- Put up House for Sale
- Put up Commercial Plot for Lease
- Put up Plot for Sale
- Put up Commercial Room for Lease
- Put up Commercial Room for Sale

#### **Buying/Renting**
- Buy a House
- Rent a House
- Rent a Commercial Plot
- Rent a Commercial Room
- Buy a Plot

---

## **Extra Features**

### **1. Rent a House with Multiple Partners**
- Shared Rent Option *(Total Rent / No. of Persons)*
- Timeline & Pooling System

### **2. Auctions by Banks**
- Properties available through bank auctions
- Bidding System

### **3. Hostel for Kids (Under 18)**
- Includes Guardian Details

---

### **Future Enhancements**
- AI-based property recommendations
- Verified Listings
- Secure Payment Gateway for Transactions

---

This structured blueprint ensures clarity and usability for seamless real estate transactions!

