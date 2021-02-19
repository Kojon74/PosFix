import React from "react";
import { StyleSheet, Text, View } from "react-native";
import Button from "./Button";

const CalibrateStartBtn = ({ calibrate, startTimer }) => {
  return (
    <View style={styles.homeBtnContainer}>
      <Button text="Calibrate" primary={false} handlePress={calibrate} />
      <Button text="Start" primary={true} handlePress={startTimer} />
    </View>
  );
};

export default CalibrateStartBtn;

const styles = StyleSheet.create({
  homeBtnContainer: {
    height: "20%",
    justifyContent: "space-between",
  },
});
