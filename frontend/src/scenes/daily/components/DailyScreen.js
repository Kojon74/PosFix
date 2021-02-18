import React from "react";
import { StyleSheet, Text, View } from "react-native";
import Overview from "./Overview";
import { Colors } from "../../../styles";
import BodyAnalysis from "./BodyAnalysis";

const DailyScreen = () => {
  const name = "ken";
  return (
    <View style={styles.container}>
      <Overview />
      <BodyAnalysis />
    </View>
  );
};

export default DailyScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.SECONDARY,
    // alignItems: "center",
    // justifyContent: "center",
  },
});
