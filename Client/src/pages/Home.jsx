import React from "react";

const services = [
  {
    name: "Maternity",
    image: "https://malaica.com/wp-content/uploads/2024/01/iStock-457087311-scaled.webp",
    description: "Comprehensive prenatal, delivery, and postnatal care for mothers and newborns.",
  },
  {
    name: "Surgery",
    image: "https://www.aimsindia.com/wp-content/uploads/2024/01/laparoscopic-surgeon-in-delhi-ncr.png",
    description: "Safe and modern surgical procedures with experienced specialists.",
  },
  {
    name: "Counseling",
    image: "https://thumbs.dreamstime.com/b/psychological-counselling-black-male-patient-depression-having-session-psychotherapist-office-african-american-man-ptsd-222886791.jpg",
    description: "Confidential therapy and emotional support by certified counselors.",
  },
  {
    name: "General Checkup",
    image: "https://bimcbali.com/wp-content/uploads/2022/12/How-Often-Should-You-Get-a-Medical-Checkup.jpg",
    description: "Routine health assessments and diagnostics to keep you in top shape.",
  },
  {
    name: "Health & Diet",
    image: "https://irp.cdn-website.com/056e16c2/dms3rep/multi/Nutrition-Counseling.png",
    description: "Personalized nutrition plans and wellness coaching.",
  },
  {
    name: "Psychiatry",
    image: "https://dy7glz37jgl0b.cloudfront.net/advice/images/betterhelp/7153/8f8ae7177ce4ead5702ce5454ab2b3d5-doctor-seeing-patient.jpg",
    description: "Mental health care including diagnosis, medication, and therapy.",
  },
  {
    name: "Dentistry",
    image: "https://pinnacledentistryco.com/wp-content/uploads/2020/09/General-Dentistry-1920-1024x683.jpg",
    description: "Preventive and corrective dental services using the latest technology.",
  },
  {
    name: "Chemotherapy",
    image: "https://media.post.rvohealth.io/wp-content/uploads/2023/06/chemotherapy-intravenous-bag-patients-receiving-treatment-732x549-thumbnail-732x549.jpg",
    description: "Cancer treatment delivered with compassion and precision.",
  },
];

const Dashboard = () => {
  return (
    <div className="ml-64 p-6 bg-[#f5faff] min-h-screen text-[#001f54] font-sans">

      <header
        className="bg-cover bg-center h-[65vh] shadow-xl flex items-center justify-center text-center px-4 mb-12"
        style={{
          backgroundImage: `url('https://cdn.pixabay.com/photo/2016/04/19/13/22/hospital-1338585_1280.jpg')`,
        }}
      >
        <div className="bg-black bg-opacity-50 p-8 rounded-xl max-w-3xl">
          <h1 className="text-4xl md:text-5xl font-extrabold text-white drop-shadow-md">
            St. Catherine Memorial Hospital
          </h1>
          <p className="mt-4 text-lg text-gray-200 font-medium">
            Committed to Compassionate, High-Quality Healthcare for All
          </p>
        </div>
      </header>

      <section className="mb-12 text-center">
        <h2 className="text-4xl font-bold text-[#001f54] mb-8">Our Services</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 px-4">
          {services.map((service, index) => (
            <div key={index} className="bg-white shadow-md rounded-xl overflow-hidden">
              <img src={service.image} alt={service.name} className="w-full h-40 object-cover" />
              <div className="p-4">
                <h3 className="text-xl font-semibold mb-2">{service.name}</h3>
                <p className="text-gray-700 text-sm">{service.description}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="bg-white shadow-md rounded-2xl p-8 mb-10">
        <h2 className="text-4xl font-bold text-[#001f54] mb-6 text-center">About Us</h2>

        <div className="flex flex-col md:flex-row items-center gap-8">
          {/* Image on the Left */}
          <div className="md:w-1/2">
            <img
              src="https://media.istockphoto.com/id/1312706413/photo/modern-hospital-building.jpg?s=612x612&amp;w=0&amp;k=20&amp;c=oUILskmtaPiA711DP53DFhOUvE7pfdNeEK9CfyxlGio="
              alt="About Us"
              className="rounded-xl shadow-lg w-full h-[500px] object-cover"
            />
          </div>

          {/* Text on the Right */}
          <div className="md:w-1/2 text-lg text-gray-700 leading-relaxed">
            <p>
              St. Catherine Memorial Hospital has served the community with excellence in healthcare for over 25 years.
              We offer a wide spectrum of services including outpatient, inpatient, surgical, maternity, pediatric, and emergency care.
            </p>
            <br />
            <p>
              Our mission is to provide compassionate, affordable, and high-quality medical care to all individuals, regardless of their background.
              We are equipped with modern technology, a team of highly trained professionals, and a passion for service that puts the patient at the center of everything we do.
            </p>
            <br />
            <p>
              From first-time visitors to long-term patients, every person is treated with dignity, empathy, and the utmost professionalism.
              We continually strive to improve outcomes and empower healthier communities through trust, care, and innovation.
            </p>
          </div>
        </div>
      </section>


      {/* Contact & Emergency Section */}
      <section className="bg-white shadow-md rounded-2xl p-8 mb-10 text-center">
        <h2 className="text-4xl font-bold text-[#001f54] mb-6">Contact Us</h2>
        <div className="space-y-2 text-lg text-gray-800">
          <p>📞 General Line: +254 712 345 678</p>
          <p>📧 Email: contact@stcatherinehospital.org</p>
          <p>🕐 Hours: Mon - Sun | 6:00 AM - 11:00 PM</p>
        </div>

        <hr className="my-6 border-gray-300" />

        <div className="space-y-2 text-lg text-red-700 font-semibold">
          <h3 className="text-2xl font-bold text-red-800 mb-2">🚨 Emergency Hotlines</h3>
          <p>🚑 Ambulance: +254 733 999 111</p>
          <p>📞 Toll-Free: 0800 721 234 (24/7 Emergency Line)</p>
          <p>👨‍⚕️ Red Cross Emergency Crew on standby</p>
        </div>

        <p className="mt-4 text-md text-gray-600 italic">
          Our Emergency Response Team operates 24/7, ensuring rapid medical assistance and close coordination with Red Cross Kenya.
        </p>
      </section>

      {/* Location Section */}
      <section className="bg-white shadow-md rounded-2xl p-8 text-center">
        <h2 className="text-3xl font-bold text-[#001f54] mb-4">Our Location</h2>
        <p className="text-gray-700 text-lg mb-4">
          We are located in Nairobi, off Ngong Road near Prestige Plaza.
        </p>
        <div className="w-full h-64 md:h-96 rounded-xl overflow-hidden shadow-lg">
          <iframe
            title="St Catherine Hospital Location"
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d15955.245584781008!2d36.7884513!3d-1.2920665!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x182f112f0c9a84e3%3A0x1f2b4d84fc9cfd48!2sNairobi%20Hospital!5e0!3m2!1sen!2ske!4v1628583924896!5m2!1sen!2ske"
            width="100%"
            height="100%"
            allowFullScreen=""
            loading="lazy"
          ></iframe>
        </div>
      </section>

      {/* Footer */}
      <footer className="text-center py-6 mt-16 text-sm text-gray-600">
        &copy; {new Date().getFullYear()} St. Catherine Memorial Hospital. All rights reserved.
      </footer>
    </div>
  );
};

export default Dashboard;


