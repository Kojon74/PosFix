import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { Colors } from "../../../styles";

const Session = ({ id, time, duration, rating, keypoints }) => {
  const secsToMins = (secs) => {
    const minutes = parseInt(secs / 60);
    const seconds = secs % 60;
    return `${minutes}m ${seconds}s`;
  };
  return (
    <View style={styles.container}>
      <View style={styles.graph} />
      <View style={styles.text}>
        <Text style={styles.time}>{time}</Text>
        <Text style={styles.duration}>{secsToMins(duration)}</Text>
        <Text style={styles.rating}>{rating}</Text>
      </View>
    </View>
  );
};

export default Session;

const styles = StyleSheet.create({
  container: {
    height: "auto",
    alignSelf: "stretch",
    marginHorizontal: 40,
    flexDirection: "row",
    borderTopWidth: 1,
    borderTopColor: Colors.PRIMARY,
  },
  graph: {
    margin: 10,
    width: 200,
    height: 200,
    backgroundColor: Colors.TERTIARY,
  },
  text: {
    margin: 10,
  },
  time: {
    marginTop: 20,
    color: Colors.PRIMARY,
    fontSize: 25,
    fontWeight: "600",
  },
  duration: {
    marginTop: 10,
    color: Colors.TERTIARY,
    fontSize: 25,
    fontWeight: "600",
  },
  rating: {
    marginTop: "auto",
    marginBottom: 20,
    color: Colors.PRIMARY,
    fontSize: 25,
    fontWeight: "800",
  },
});
