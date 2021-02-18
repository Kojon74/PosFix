import React, { useEffect, useState } from "react";
import { StyleSheet, Text, View } from "react-native";
import { Colors } from "../../../styles";
import PerformanceBar from "./PerformanceBar";

const Overview = () => {
  const [date, setDate] = useState(null);
  const [timeSeated, setTimeSeated] = useState(500);

  useEffect(() => {
    const dateObj = new Date();
    setDate(
      `${dateObj.toLocaleString("default", {
        month: "long",
      })} ${dateObj.getDate()}, ${dateObj.getFullYear()}`
    );
  }, []);

  const timeInHrs = (minutes) => {
    const hours = parseInt(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
  };
  return (
    <View style={styles.container}>
      <PerformanceBar percent={50} />
      <View>
        <Text style={styles.date}>{date}</Text>
        <Text style={styles.time}>{timeInHrs(timeSeated)}</Text>
        <Text style={styles.date}>Time spent seated</Text>
      </View>
    </View>
  );
};

export default Overview;

const styles = StyleSheet.create({
  container: {
    marginHorizontal: 40,
    paddingVertical: 10,
    flexDirection: "row",
    justifyContent: "space-around",
    borderBottomWidth: 1,
    borderBottomColor: Colors.PRIMARY,
  },
  date: {
    color: Colors.PRIMARY,
    opacity: 0.5,
    fontSize: 18,
    fontWeight: "500",
  },
  time: {
    marginTop: 30,
    color: Colors.TERTIARY,
    fontSize: 25,
    fontWeight: "700",
  },
});
