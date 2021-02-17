import React from "react";
import { StyleSheet, Text, View } from "react-native";
import { Colors } from "../styles";

import TabBar from "./TabBar";

const NavBar = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.header}>PosFix</Text>
      <TabBar />
    </View>
  );
};

export default NavBar;

const styles = StyleSheet.create({
  container: { flex: 1 },
  header: {
    marginLeft: 30,
    marginTop: 10,
    color: Colors.PRIMARY,
    fontSize: 30,
    fontWeight: "700",
  },
});
