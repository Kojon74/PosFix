import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { Colors } from "../../../styles";

const DataScreen = () => {
  return (
    <View style={styles.container}>
      <View style={styles.borderBottom}>
        <View style={styles.headerContainer}>
          <Text style={styles.header}>Sessions</Text>
        </View>
      </View>
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
