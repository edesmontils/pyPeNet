<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="1.1">
    <xsl:output method="text"/>
    <xsl:variable name='nl'><xsl:text>&#xa;</xsl:text></xsl:variable>
    <xsl:template match="/" >
        <xsl:text>name;type;v1;v2;v3</xsl:text><xsl:value-of select="$nl"/>
        <xsl:apply-templates select="/pnml/net/place"/>
        <xsl:apply-templates select="/pnml/net/transition"/>
        <xsl:apply-templates select="/pnml/net/arc"/>
    </xsl:template>
    <xsl:template match="place">
        <xsl:variable name="id" select="@id"/>
        <xsl:variable name='init' select="substring-after(initialMarking/value, ',')"/>
        <xsl:value-of select="concat($id,';place;',$init,';;',$nl)"/>
    </xsl:template>
    <xsl:template match="transition">
        <xsl:variable name="id" select="@id"/>
        <xsl:variable name='prio' select="priority/value/text()"/>
        <xsl:value-of select="concat($id,';transition;',$prio,';;',$nl)"/>
    </xsl:template>
    <xsl:template match="arc">
        <xsl:variable name="id" select="@id"/>
        <xsl:variable name="source" select="@source"/>
        <xsl:variable name="cible" select="@target"/>
        <xsl:variable name="poids" select="substring-after(inscription/value, ',')"/>
        <xsl:variable name="type" select="type/@value"/>
        <xsl:value-of select="concat($id,';',$type,';',$source,';',$cible,';',$poids,$nl)"/>
    </xsl:template>
</xsl:stylesheet>