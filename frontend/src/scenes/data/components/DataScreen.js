import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { Colors } from "_styles";

const DataScreen = () => {
  return (
    <View style={styles.container}>
      <Text>Data</Text>
    </View>
  );
};

export default DataScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.SECONDARY,
    alignItems: "center",
    justifyContent: "center",
  },
});
