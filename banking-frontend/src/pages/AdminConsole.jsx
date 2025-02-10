import React, { useState, useEffect } from "react";
import emailjs from 'emailjs-com'; // Import EmailJS
import "../Console.css";

export default function AdminConsole() {
  const [applications, setApplications] = useState([]);

  useEffect(() => {
    fetchApplications();
  }, []);

  const fetchApplications = async () => {
    try {
      const response = await fetch("http://localhost:5000/admin_console");
      if (response.ok) {
        const data = await response.json();
        setApplications(data);
      } else {
        console.error("Error fetching applications:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching applications:", error);
    }
  };

  const sendEmail = (toEmail, subject, message) => {
    const emailJsConfig = {
      userId: "duGyQMPA15QXvU-LA", // Your EmailJS User ID
      serviceId: "default_service", // Your EmailJS Service ID
      templateId: "template_jwoiro3", // Your EmailJS Template ID
    };

    // Prepare email parameters
    const emailParams = {
      to_email: toEmail,
      subject: subject,
      message: message,
    };

    // Send email via EmailJS
    emailjs.send(
      emailJsConfig.serviceId,
      emailJsConfig.templateId,
      emailParams,
      emailJsConfig.userId
    )
    .then(
      (response) => {
        console.log("Email sent successfully:", response);
        alert(message);  // Show a success message to the admin
      },
      (error) => {
        console.error("Error sending email:", error);
        alert("Failed to send email.");
      }
    );
  };

  const handleApprove = async (id, email) => {
    try {
      const response = await fetch(
        `http://localhost:5000/admin_console/approve/${id}`,
        {
          method: "POST",
        }
      );
      const data = await response.json();

      if (response.ok) {
        // Send Approval Email
        sendEmail(email, "Your Application has been Approved", "Congratulations! Your application for a card has been approved.");
        alert(`Application approved! Email sent: ${data.message}`);
      } else {
        alert(`Approval failed: ${data.message}`);
      }

      fetchApplications();
    } catch (error) {
      console.error("Error approving application:", error);
      alert("Failed to approve application");
    }
  };

  const handleReject = async (id, email) => {
    try {
      const response = await fetch(
        `http://localhost:5000/admin_console/reject/${id}`,
        {
          method: "POST",
        }
      );
      const data = await response.json();

      if (response.ok) {
        // Send Rejection Email
        sendEmail(email, "Your Application has been Rejected", "We're sorry, but your application for a card has been rejected.");
        alert(`Application rejected! Email sent: ${data.message}`);
      } else {
        alert(`Rejection failed: ${data.message}`);
      }

      fetchApplications();
    } catch (error) {
      console.error("Error rejecting application:", error);
      alert("Failed to reject application");
    }
  };

  return (
    <div>
      <h1>Admin Console</h1>
      <h2>Card Applications</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Card Type</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {applications.map((app) => (
            <tr key={app._id}>
              <td>{app.name}</td>
              <td>{app.email}</td>
              <td>{app.cardType}</td>
              <td>{app.status || "Pending"}</td>
              <td>
                {app.status === "Pending" && (
                  <>
                    <button onClick={() => handleApprove(app._id, app.email)}>
                      Approve
                    </button>
                    <button onClick={() => handleReject(app._id, app.email)}>
                      Reject
                    </button>
                  </>
                )}
                {app.status && <span>{app.status}</span>}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
