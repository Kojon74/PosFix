import React from "react";
import { StyleSheet, Text, ScrollView } from "react-native";
import Session from "./Session";
import sessions from "../../../../data";

const SessionContainer = () => {
  return (
    <ScrollView style={styles.container}>
      {sessions.map((session) => {
        return <Session key={session.id} {...session} />;
      })}
    </ScrollView>
  );
};

export default SessionContainer;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignSelf: "stretch",
  },
});
