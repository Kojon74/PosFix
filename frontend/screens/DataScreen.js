import React from "react";
import { StyleSheet, Text, View } from "react-native";

const DataScreen = () => {
  return (
    <View style={styles.container}>
      <Text>Data</Text>
    </View>
  );
};

export default DataScreen;

const colors = { primary: "#05386B", secondary: "#5CDB95" };

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.secondary,
    alignItems: "center",
    justifyContent: "center",
  },
});
