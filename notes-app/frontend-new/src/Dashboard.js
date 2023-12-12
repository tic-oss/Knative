import React, { useState } from "react";
import { Box, Text, Divider, Grid } from "@chakra-ui/react";
import EventCard from "./EventCard";
import EventPopup from "./EventPopup";

const Dashboard = ({ schedules }) => {
  const [selectedEvent, setSelectedEvent] = useState(null);

  const handleCardClick = (event) => {
    setSelectedEvent(event);
  };

  const handleClosePopup = () => {
    setSelectedEvent(null);
  };

  // const currentDate = new Date();

  // const expiredReminders = schedules.filter((event) => {
  //   console.log(event);
  //   const eventDate = new Date(`${event.date} ${event.time}`);
  //   return eventDate <= currentDate;
  // });

  // const upcomingReminders = schedules.filter((event) => {
  //   console.log(event.date, "popopop");
  //   const eventDate = new Date(`${event.date} ${event.time}`);
  //   return eventDate > currentDate;
  // });

  return (
    <Box p={4}>
      <Text fontSize="2xl" fontWeight="bold" mb={4}>
        Dashboard
      </Text>

      {schedules.length > 0 && (
        <>
          <Text fontSize="lg" fontWeight="bold" mb={2}>
            Upcoming Reminders
          </Text>
          <Divider mb={4} />
          <Grid templateColumns="repeat(auto-fill, minmax(250px, 1fr))" gap={4}>
            {schedules
              .filter((event) => event.expired === false)
              .map((event) => (
                <EventCard
                  key={event.title}
                  event={event}
                  onCardClick={() => handleCardClick(event)}
                />
              ))}
          </Grid>
        </>
      )}

      {schedules.length > 0 && (
        <>
          <Text
            fontSize="lg"
            fontWeight="bold"
            mb={2}
            mt={schedules.length > 0 ? 8 : 0}
          >
            Expired Reminders
          </Text>
          <Divider mb={4} />
          <Grid templateColumns="repeat(auto-fill, minmax(250px, 1fr))" gap={4}>
            {schedules
              .filter((event) => event.expired === true)
              .map((event) => (
                <EventCard
                  key={event.title}
                  event={event}
                  onCardClick={() => handleCardClick(event)}
                />
              ))}
          </Grid>
        </>
      )}

      {selectedEvent && (
        <EventPopup
          isOpen={true}
          onClose={handleClosePopup}
          event={selectedEvent}
        />
      )}
    </Box>
  );
};

export default Dashboard;
