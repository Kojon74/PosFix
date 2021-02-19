import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { Colors } from "../../../styles";
import SessionContainer from "./SessionContainer";

const DataScreen = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.header}>Sessions</Text>
      <SessionContainer />
    </View>
  );
};

export default DataScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.SECONDARY,
    alignItems: "center",
  },
  borderBottom: {
    marginHorizontal: 40,
    flexDirection: "row",
    justifyContent: "center",
    borderBottomWidth: 1,
    borderBottomColor: Colors.PRIMARY,
  },
  headerContainer: {
    flex: 1,
    alignItems: "center",
  },
  header: {
    paddingBottom: 10,
    color: Colors.PRIMARY,
    fontSize: 25,
    fontWeight: "500",
  },
});
