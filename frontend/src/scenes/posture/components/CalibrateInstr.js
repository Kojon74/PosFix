import React from "react";
import { FlatList, StyleSheet, Text, View } from "react-native";
import { Colors } from "../../../styles";
import Button from "./Button";

const CalibrateInstr = ({ setIsCalibrating }) => {
  const instr = [
    { key: "Sit up straight" },
    { key: "Slightly tighten your glutes" },
    { key: "Tuck your neck slightly" },
    { key: "Hold for 10 seconds" },
  ];

  const handleCancel = () => {
    setIsCalibrating(false);
  };

  return (
    <View>
      <Text style={styles.calibrating}>Calibrating...</Text>
      <View style={styles.instrContainer}>
        <Text style={styles.header}>Follow the instructions below:</Text>
        <FlatList
          data={instr}
          renderItem={({ item, index }) => (
            <Text style={styles.instr}>{`${index + 1}. ${item.key}`}</Text>
          )}
        />
      </View>
      <Button
        text="Cancel"
        primary={false}
        handlePress={handleCancel}
        style={styles.cancelBtn}
      />
    </View>
  );
};

export default CalibrateInstr;

const styles = StyleSheet.create({
  container: {
    alignItems: "center",
  },
  calibrating: {
    marginTop: -125,
    marginBottom: 100,
    alignSelf: "center",
    justifyContent: "flex-start",
    color: Colors.PRIMARY,
    fontSize: 30,
    fontWeight: "600",
  },
  instrContainer: {
    width: 275,
    paddingHorizontal: 30,
    paddingVertical: 10,
    borderRadius: 10,
    backgroundColor: Colors.TERTIARY,
    alignItems: "flex-start",
    justifyContent: "center",
  },
  header: {
    marginVertical: 10,
    color: Colors.PRIMARY,
    fontSize: 20,
    fontWeight: "600",
  },
  instr: {
    fontSize: 15,
    marginVertical: 3,
  },
  cancelBtn: {
    marginTop: 10,
    alignSelf: "center",
  },
});
