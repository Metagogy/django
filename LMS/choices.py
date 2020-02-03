OCCUPATION_CHOICES = (
    (1, ("Student")),
    (2, ("Employee"))
)
LOCATION_CHOICES = (
	(1,("Vijayawada")),
	(2,("Kodada"))
)


locations = [
        {
        "id":0,
        "text": "Andhra Pradesh",
        },
        {
        "id":1,
        "text": "Arunachal Pradesh",
        },
        {
        "id":2,
        "text": "Bihar",
        },
        {
        "id":3,
        "text": "Chhattisgarh",
        },
        {
        "id":4,
        "text": "Goa",
        },
        {
        "id":5,
        "text": "Gujarat",
        },
        {
        "id":6,
        "text": "Haryana",
        },
        {
        "id":7,
        "text": "Jammu and Kashmir",
        },
        {
        "id":8,
        "text": "Jharkhand",
        },
        {
        "id":9,
        "text": "Karnataka",
        },
        {
        "id":10,
        "text": "Kerala",
        },
        {
        "id":11,
        "text": "Madhya Pradesh",
        },
        {
        "id":12,
        "text": "Maharashtra",
        },
        {
        "id":13,
        "text": "Manipur",
        },
        {
        "id":14,
        "text": "Meghalaya",
        },
        {
        "id":15,
        "text": "Mizoram",
        },
        {
        "id":16,
        "text": "Nagaland",
        },
        {
        "id":17,
        "text": "Odisha",
        },
        {
        "id":18,
        "text": "Punjab",
        },
        {
        "id":19,
        "text": "Rajasthan",
        },
        {
        "id":20,
        "text": "Sikkim",
        },
        {
        "id":21,
        "text": "Tamil Nadu",
        },
        {
        "id":22,
        "text": "Telangana",
        },
        {
        "id":23,
        "text": "Tripura",
        },
        {
        "id":24,
        "text": "Uttarakhand",
        },
        {
        "id":25,
        "text": "Uttar Pradesh",
        },
        {
        "id":26,
        "text": "West Bengal",
        },
        {
        "id":27,
        "text": "Andaman and Nicobar Island",
        },
        {
        "id":28,
        "text": "Chandigarh",
        },
        {
        "id":29,
        "text": "Dadra and Nagar Haveli",
        },
        {
        "id":30,
        "text": "Daman and Diu",
        },
        {
        "id":31,
        "text": "Delhi",
        },
        {
        "id":32,
        "text": "Lakshadweep",
        },
        {
        "id":33,
        "text": "Puducherry",
        }

]
occupation=[
        {
        "id":0,
        "text": "Student",
        },
        {
        "id":1,
        "text": "Employee",
        }]
class StatesOfIndia(object):
    STATES = {
        "Andhra Pradesh":"Andhra Pradesh",
		"Arunachal Pradesh ":"Arunachal Pradesh ",
		"Assam":"Assam",
		"Bihar":"Bihar",
		"Chhattisgarh":"Chhattisgarh",
		"Goa":"Goa",
		"Gujarat":"Gujarat",
		"Haryana":"Haryana",
		"Himachal Pradesh":"Himachal Pradesh",
		"Jammu and Kashmir ":"Jammu and Kashmir ",
		"Jharkhand":"Jharkhand",
		"Karnataka":"Karnataka",
		"Kerala":"Kerala",
		"Madhya Pradesh":"Madhya Pradesh",
		"Maharashtra":"Maharashtra",
		"Manipur":"Manipur",
		"Meghalaya":"Meghalaya",
		"Mizoram":"Mizoram",
		"Nagaland":"Nagaland",
		"Odisha":"Odisha",
		"Punjab":"Punjab",
		"Rajasthan":"Rajasthan",
		"Sikkim":"Sikkim",
		"Tamil Nadu":"Tamil Nadu",
		"Telangana":"Telangana",
		"Tripura":"Tripura",
		"Uttar Pradesh":"Uttar Pradesh",
		"Uttarakhand":"Uttarakhand",
		"West Bengal":"West Bengal"

        }

    @staticmethod
    def get_state_names():
        return StatesOfIndia.STATES.keys()