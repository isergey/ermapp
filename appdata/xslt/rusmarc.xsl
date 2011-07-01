<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:marc="http://www.loc.gov/MARC21/slim"
                xmlns:exsl="http://exslt.org/common"
                exclude-result-prefixes="marc exsl">
<xsl:output
        method="html"
        indent="yes"
        encoding="utf-8"
        standalone="no"
        omit-xml-declaration="no"
        />

<xsl:param name="ind" select="''"/>
<!--
RUSMARC
-->
<xsl:template name="rusmarc">
    <xsl:choose>
        <xsl:when test="$fmt='M'">
            <xsl:call-template name="dump">
                <xsl:with-param name="r" select="."/>
            </xsl:call-template>
        </xsl:when>
        <xsl:otherwise>
            <xsl:variable name="bl" select="leader/leader07"/>
            <xsl:variable name="type" select="leader/type"/>
            <xsl:choose>
                <xsl:when test="$type='x' or $type='y' or $type='z'">
                    <!-- Authority record -->
                    <!--
                              <xsl:call-template name="authority"/>
                    -->
                </xsl:when>
                <xsl:otherwise>
                    <!-- Bibliographic record -->
                    <xsl:choose>
                        <xsl:when test="$bl='a'">
                            <xsl:call-template name="analytics"/>
                        </xsl:when>
                        <xsl:when test="$bl='m'">
                            <xsl:call-template name="monograph"/>
                        </xsl:when>
                        <xsl:when test="$bl='s'">
                            <xsl:call-template name="serial"/>
                        </xsl:when>
                        <xsl:when test="$bl='c'">
                            <xsl:call-template name="monograph"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:call-template name="monograph"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:if test="$fmt='F'">
                <xsl:if test="$subject">
                    <xsl:call-template name="subjects"/>
                </xsl:if>
                <xsl:if test="$holdings and count(../../holdingsData) = 0">
                    <!--
                              <xsl:apply-templates select="field[@id='899']"/>
                    -->
                    <xsl:call-template name="holdings"/>
                </xsl:if>
            </xsl:if>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template name="gen">
    <xsl:param name="r" select="/.."/>
    <xsl:param name="s" select="/.."/>
    <xsl:param name="pub" select="'all'"/>
    <xsl:param name="na" select="true()"/>
    <xsl:if test="$na">
        <xsl:apply-templates select="$r/subfield[@id='1']/field[@id='700']"/>
        <xsl:apply-templates select="$r/subfield[@id='1']/field[@id='710']"/>
    </xsl:if>
    <xsl:call-template name="title">
        <xsl:with-param name="s1" select="$r/subfield[@id='1']/field[@id='200']"/>
        <xsl:with-param name="s2" select="$s"/>
    </xsl:call-template>
    <xsl:apply-templates select="$r/subfield[@id='1']/field[@id='205']"/>
    <xsl:apply-templates select="$r/subfield[@id='1']/field[@id='230']"/>
    <xsl:choose>
        <xsl:when test="$pub='all'">
            <xsl:apply-templates select="$r/subfield[@id='1']/field[@id='210']"/>
        </xsl:when>
        <xsl:when test="$pub='place'">
            <xsl:text>.-</xsl:text>
            <xsl:choose>
                <xsl:when test="count($r/subfield[@id='1']/field[@id='210']/subfield[@id='a']) &gt; 0">
                    <xsl:for-each select="$r/subfield[@id='1']/field[@id='210']/subfield[@id='a']">
                        <xsl:choose>
                            <xsl:when test="position() = 1">
                                <xsl:value-of select="."/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:text>;</xsl:text>
                                <xsl:value-of select="."/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:for-each>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SINE_LOCO']"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:when>
        <xsl:otherwise>
            <xsl:if test="count($r/subfield[@id='1']/field[@id='210']/subfield[@id='d'])">
                <xsl:text>.-</xsl:text>
                <xsl:value-of select="$r/subfield[@id='1']/field[@id='210']/subfield[@id='d']"/>
            </xsl:if>
        </xsl:otherwise>
    </xsl:choose>
    <xsl:apply-templates select="$r/subfield[@id='1']/field[@id='215']"/>
    <xsl:apply-templates select="$r/subfield[@id='1']/field[@id='225']"/>
    <xsl:apply-templates select="$r/subfield[@id='1']/field[@id='010']"/>
    <xsl:if test="$na">
        <xsl:apply-templates select="$r/subfield[@id='1']/field[@id='011']"/>
        <xsl:apply-templates select="$s/subfield[@id='1']/field[@id='011']"/>
    </xsl:if>
    <!--<xsl:apply-templates select="$r/subfield[@id='1']/field[@id='856']"/>-->
    <xsl:text>.</xsl:text>
</xsl:template>

<xsl:template name="spec">
    <xsl:param name="pub" select="'all'"/>
    <xsl:apply-templates select="field[@id='700']"/>
    <xsl:apply-templates select="field[@id='710']"/>
    <xsl:call-template name="title">
        <xsl:with-param name="s1" select="field[@id='200']"/>
    </xsl:call-template>
    <xsl:apply-templates select="field[@id='205']"/>
    <xsl:apply-templates select="field[@id='230']"/>
    <xsl:choose>
        <xsl:when test="$pub='all'">
            <xsl:apply-templates select="field[@id='210']"/>
        </xsl:when>
        <xsl:otherwise>
            <xsl:if test="count(field[@id='210']/subfield[@id='d'])">
                <xsl:text>.-</xsl:text>
                <xsl:value-of select="field[@id='210']/subfield[@id='d']"/>
            </xsl:if>
        </xsl:otherwise>
    </xsl:choose>
    <xsl:apply-templates select="field[@id='215']"/>
    <xsl:apply-templates select="field[@id='225']"/>

    <xsl:call-template name="notes"/>

    <xsl:if test="$fmt != 'B' and count(field[@id='464']) &gt; 0">
        <xsl:for-each select="field[@id='464']">
            <xsl:choose>
                <xsl:when test="count(subfield[@id='1']/controlfield[@id='001']) &gt; 0 and $ht">
                    <a href="follow+{subfield[@id='1']/controlfield[@id='001']}[1,12]+{$lang}">
                        <xsl:call-template name="gen">
                            <xsl:with-param name="r" select="."/>
                        </xsl:call-template>
                    </a>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:call-template name="gen">
                        <xsl:with-param name="r" select="."/>
                    </xsl:call-template>
                </xsl:otherwise>
            </xsl:choose>
            <br/>
        </xsl:for-each>
        <p/>
    </xsl:if>
    <xsl:call-template name="links"/>

    <xsl:apply-templates select="field[@id='010']"/>
    <xsl:apply-templates select="field[@id='011']"/>
    <!--<xsl:apply-templates select="field[@id='856']"/>-->
    <xsl:text>.</xsl:text>
</xsl:template>

<xsl:template name="sub">
    <xsl:if test="count(field[@id='463']) &gt; 0">
        <p>
            <table>
                <xsl:for-each select="field[@id='463']">
                    <tr>
                        <td>
                            <xsl:choose>
                                <xsl:when
                                        test="count(subfield[@id='1']/controlfield[@id='001']) &gt; 0 and $fmt != 'B' and $ht">
                                    <a href="follow+{subfield[@id='1']/controlfield[@id='001']}[1,12]+{$lang}">
                                        <xsl:call-template name="gen">
                                            <xsl:with-param name="r" select="."/>
                                            <xsl:with-param name="pub" select="'year'"/>
                                        </xsl:call-template>
                                    </a>
                                </xsl:when>
                                <xsl:otherwise>
                                    <xsl:call-template name="gen">
                                        <xsl:with-param name="r" select="."/>
                                        <xsl:with-param name="pub" select="'year'"/>
                                    </xsl:call-template>
                                </xsl:otherwise>
                            </xsl:choose>
                        </td>
                    </tr>
                </xsl:for-each>
            </table>
        </p>
    </xsl:if>
</xsl:template>

<xsl:template name="issue">
    <xsl:param name="year" select="true()"/>
    <xsl:if test="count(subfield[@id='1']/field[@id='210']/subfield[@id='d']) and $year">
        <xsl:value-of select="subfield[@id='1']/field[@id='210']/subfield[@id='d']"/>
        <xsl:if test="count(subfield[@id='1']/field[@id='200']) &gt; 0">
            <xsl:text>.-</xsl:text>
        </xsl:if>
    </xsl:if>
    <xsl:call-template name="title">
        <xsl:with-param name="s1" select="subfield[@id='1']/field[@id='200']"/>
    </xsl:call-template>
</xsl:template>

<xsl:template name="htitle">
    <xsl:param name="r" select="/.."/>
    <xsl:for-each select="$r/subfield[@id='1']/field[@id='200']">
        <xsl:call-template name="title">
            <xsl:with-param name="s1" select="."/>
        </xsl:call-template>
    </xsl:for-each>
    <xsl:text>.-</xsl:text>
    <xsl:choose>
        <xsl:when test="count($r/subfield[@id='1']/field[@id='210']/subfield[@id='a']) &gt; 0">
            <xsl:for-each select="$r/subfield[@id='1']/field[@id='210']/subfield[@id='a']">
                <xsl:choose>
                    <xsl:when test="position() = 1">
                        <xsl:value-of select="."/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>;</xsl:text>
                        <xsl:value-of select="."/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
        </xsl:when>
        <xsl:otherwise>
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SINE_LOCO']"/>
        </xsl:otherwise>
    </xsl:choose>
    <xsl:text>,</xsl:text>
    <xsl:choose>
        <xsl:when test="count($r/subfield[@id='1']/field[@id='210']/subfield[@id='d']) &gt; 0">
            <xsl:value-of select="$r/subfield[@id='1']/field[@id='210']/subfield[@id='d']"/>
        </xsl:when>
        <xsl:otherwise>
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SINE_ANNO']"/>
        </xsl:otherwise>
    </xsl:choose>
    <xsl:apply-templates select="$r/subfield[@id='1']/field[@id='225']"/>
</xsl:template>

<!-- Derived from template for field 200 -->
<xsl:template name="title">
    <xsl:param name="s1" select="/.."/>
    <xsl:param name="s2" select="/.."/>
    <xsl:for-each select="$s1/subfield[@id='a']">
        <xsl:if test="position() != 1">
            <xsl:text>;</xsl:text>
        </xsl:if>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="$s2/subfield[@id='1']/field[@id='200']">
        <xsl:text>.</xsl:text>
        <xsl:call-template name="title">
            <xsl:with-param name="s1" select="."/>
        </xsl:call-template>
    </xsl:for-each>
    <xsl:for-each select="$s1/subfield[@id='b']">
        <xsl:text> [</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>]</xsl:text>
    </xsl:for-each>
    <xsl:for-each select="$s1/subfield[@id='d']">
        <xsl:text> =</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="$s1/subfield[@id='h']">
        <xsl:text>.</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="$s1/subfield[@id='i']">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>,</xsl:text>
                <xsl:value-of select="."/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>.</xsl:text>
                <xsl:value-of select="."/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:for-each>
    <xsl:for-each select="$s1/subfield[@id='e']">
        <xsl:text>:</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:if test="count($s1/subfield[@id='f']) &gt; 0 or count($s1/subfield[@id='g']) &gt; 0">
        <xsl:text> /</xsl:text>
        <xsl:for-each select="$s1/subfield[@id='f']">
            <xsl:choose>
                <xsl:when test="position() = 1">
                    <xsl:value-of select="."/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:text>;</xsl:text>
                    <xsl:value-of select="."/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:for-each>
        <xsl:for-each select="$s1/subfield[@id='g']">
            <xsl:text>;</xsl:text>
            <xsl:value-of select="."/>
        </xsl:for-each>
    </xsl:if>
    <xsl:if test="$s1/../../../leader/leader07 = 'a'">
        <xsl:for-each select="$s1/subfield[@id='v']">
            <xsl:text>.-</xsl:text>
            <xsl:value-of select="."/>
        </xsl:for-each>
    </xsl:if>
</xsl:template>

<xsl:template name="monograph">
    <xsl:choose>
        <xsl:when test="count(field[@id='461']/subfield[@id='1']) &gt; 0">
            <xsl:variable name="volnum" select="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='v']"/>
            <xsl:variable name="havetitle" select="field[@id='200']/indicator[@id='1']"/>
            <xsl:choose>
                <xsl:when
                        test="count(field[@id='461']/subfield[@id='1']/controlfield[@id='001']) &gt; 0 and $fmt != 'B' and $ht">
                    <a href="follow+{field[@id='461']/subfield[@id='1']/controlfield[@id='001']}[1,12]+{$lang}">
                        <xsl:call-template name="gen">
                            <xsl:with-param name="r" select="field[@id='461']"/>
                        </xsl:call-template>
                    </a>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:call-template name="gen">
                        <xsl:with-param name="r" select="field[@id='461']"/>
                    </xsl:call-template>
                </xsl:otherwise>
            </xsl:choose>
            <p>
                <xsl:if test="string-length($volnum) &gt; 0 and $havetitle='1'">
                    <xsl:value-of select="$volnum"/>
                    <xsl:text>:</xsl:text>
                </xsl:if>
                <xsl:call-template name="spec">
                    <xsl:with-param name="pub" select="'year'"/>
                </xsl:call-template>
            </p>
        </xsl:when>
        <xsl:otherwise>
            <xsl:call-template name="spec"/>
            <xsl:for-each select="field[@id='463']">
                <p>
                    <xsl:choose>
                        <xsl:when
                                test="count(subfield[@id='1']/controlfield[@id='001']) &gt; 0 and $fmt != 'B' and $ht">
                            <a href="follow+{subfield[@id='1']/controlfield[@id='001']}[1,12]+{lang}">
                                <xsl:call-template name="gen">
                                    <xsl:with-param name="r" select="."/>
                                    <xsl:with-param name="pub" select="'year'"/>
                                </xsl:call-template>
                            </a>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:call-template name="gen">
                                <xsl:with-param name="r" select="."/>
                                <xsl:with-param name="pub" select="'year'"/>
                            </xsl:call-template>
                        </xsl:otherwise>
                    </xsl:choose>
                </p>
            </xsl:for-each>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template name="serial">
    <xsl:choose>
        <xsl:when test="count(field[@id='461']/subfield[@id='1']) &gt; 0">
            <xsl:variable name="volnum">
                <xsl:choose>
                    <xsl:when
                            test="count(field[@id='462']/subfield[@id='1']/field[@id='200']/subfield[@id='v']) &gt; 0">
                        <xsl:value-of select="field[@id='462']/subfield[@id='1']/field[@id='200']/subfield[@id='v']"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="field[@id='461']/subfield[@id='1']/field[@id='200']/subfield[@id='v']"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:variable>
            <xsl:variable name="havetitle" select="field[@id='200']/indicator[@id='1']"/>
            <xsl:choose>
                <xsl:when
                        test="count(field[@id='461']/subfield[@id='1']/controlfield[@id='001']) &gt; 0 and $fmt != 'B' and $ht">
                    <a href="follow+{field[@id='461']/subfield[@id='1']/controlfield[@id='001']}[1,12]+{$lang}">
                        <xsl:call-template name="gen">
                            <xsl:with-param name="r" select="field[@id='461']"/>
                            <xsl:with-param name="s" select="field[@id='462']"/>
                        </xsl:call-template>
                    </a>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:call-template name="gen">
                        <xsl:with-param name="r" select="field[@id='461']"/>
                        <xsl:with-param name="s" select="field[@id='462']"/>
                    </xsl:call-template>
                </xsl:otherwise>
            </xsl:choose>
            <p>
                <xsl:if test="string-length($volnum) &gt; 0 and $havetitle='1'">
                    <xsl:value-of select="$volnum"/>
                    <xsl:text>:</xsl:text>
                </xsl:if>
                <xsl:call-template name="spec">
                    <xsl:with-param name="pub" select="'year'"/>
                </xsl:call-template>
                <xsl:call-template name="sub"/>
            </p>
        </xsl:when>
        <xsl:otherwise>
            <xsl:call-template name="spec"/>
            <xsl:call-template name="sub"/>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template name="analytics">
    <xsl:apply-templates select="field[@id='700']"/>
    <xsl:apply-templates select="field[@id='710']"/>
    <xsl:call-template name="title">
        <xsl:with-param name="s1" select="field[@id='200']"/>
    </xsl:call-template>
    <xsl:apply-templates select="field[@id='205']"/>
    <xsl:apply-templates select="field[@id='230']"/>
    <xsl:text> //</xsl:text>
    <xsl:choose>
        <xsl:when test="count(field[@id='461']/subfield[@id='1']) &gt; 0">
            <xsl:choose>
                <xsl:when
                        test="count(field[@id='461']/subfield[@id='1']/controlfield[@id='001']) &gt; 0 and $fmt != 'B' and $ht">
                    <a href="follow+{field[@id='461']/subfield[@id='1']/controlfield[@id='001']}[1,12]+{$lang}">
                        <xsl:call-template name="gen">
                            <xsl:with-param name="r" select="field[@id='461']"/>
                            <xsl:with-param name="s" select="field[@id='462']"/>
                            <xsl:with-param name="pub" select="'place'"/>
                            <xsl:with-param name="na" select="false()"/>
                        </xsl:call-template>
                    </a>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:call-template name="gen">
                        <xsl:with-param name="r" select="field[@id='461']"/>
                        <xsl:with-param name="s" select="field[@id='462']"/>
                        <xsl:with-param name="pub" select="'place'"/>
                        <xsl:with-param name="na" select="false()"/>
                    </xsl:call-template>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:for-each select="field[@id='463']">
                <xsl:choose>
                    <xsl:when test="position() != 1">
                        <xsl:text>;</xsl:text>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>.-</xsl:text>
                    </xsl:otherwise>
                </xsl:choose>
                <xsl:choose>
                    <xsl:when test="count(subfield[@id='1']/controlfield[@id='001']) &gt; 0 and $fmt != 'B' and $ht">
                        <a href="follow+{subfield[@id='1']/controlfield[@id='001']}[1,12]+{$lang}">
                            <xsl:call-template name="issue"/>
                        </a>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:call-template name="issue"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
        </xsl:when>
        <xsl:otherwise>
            <xsl:choose>
                <xsl:when
                        test="count(field[@id='463']/subfield[@id='1']/controlfield[@id='001']) &gt; 0 and $fmt != 'B' and $ht">
                    <a href="follow+{field[@id='463']/subfield[@id='1']/controlfield[@id='001']}[1,12]+{$lang}">
                        <xsl:call-template name="htitle">
                            <xsl:with-param name="r" select="field[@id='463']"/>
                            <xsl:with-param name="na" select="false()"/>
                        </xsl:call-template>
                    </a>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:call-template name="htitle">
                        <xsl:with-param name="r" select="field[@id='463']"/>
                        <xsl:with-param name="na" select="false()"/>
                    </xsl:call-template>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:otherwise>
    </xsl:choose>
    <xsl:apply-templates select="field[@id='215']"/>
    <xsl:apply-templates select="field[@id='225']"/>
    <xsl:apply-templates select="field[@id='461']/subfield[@id='1']/field[@id='011']"/>
    <xsl:apply-templates select="field[@id='463']/subfield[@id='1']/field[@id='011']"/>
    <xsl:call-template name="notes"/>
    <!--<xsl:apply-templates select="field[@id='856']"/>-->
    <xsl:text>.</xsl:text>
</xsl:template>

<xsl:template name="collection">
    <span class="warn"><xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='W_UNIMPL']"/></span>
</xsl:template>

<xsl:template name="subjects">
    <xsl:variable name="p600" select="count(field[@id='600'])"/>
    <xsl:variable name="p601" select="count(field[@id='601'])"/>
    <xsl:variable name="p602" select="count(field[@id='602'])"/>
    <xsl:variable name="p606" select="count(field[@id='606'])"/>
    <xsl:variable name="p607" select="count(field[@id='607'])"/>
    <xsl:variable name="p610" select="count(field[@id='610'])"/>
    <p/>
    <xsl:if test="$p600 + $p601 + $p602 + $p606 + $p607 + $p610 &gt; 0">
        <xsl:text>– –</xsl:text>
    </xsl:if>
    <xsl:for-each select="field[@id='600']">
        <xsl:text></xsl:text>
        <xsl:value-of select="position()"/>
        <xsl:text>.</xsl:text>
        <xsl:value-of select="subfield[@id='a']"/>
        <xsl:choose>
            <xsl:when test="count(subfield[@id='g']) &gt; 0">
                <xsl:text>,</xsl:text>
                <xsl:value-of select="subfield[@id='g']"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:if test="count(subfield[@id='b']) &gt; 0">
                    <xsl:text>,</xsl:text>
                    <xsl:value-of select="subfield[@id='b']"/>
                </xsl:if>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:if test="count(subfield[@id='d']) &gt; 0">
            <xsl:text></xsl:text>
            <xsl:value-of select="subfield[@id='d']"/>
        </xsl:if>
        <xsl:if test="count(subfield[@id='c']) &gt; 0">
            <xsl:text> (</xsl:text>
            <xsl:for-each select="subfield[@id='c']">
                <xsl:if test="position() != 1">
                    <xsl:text> ,</xsl:text>
                </xsl:if>
                <xsl:value-of select="."/>
            </xsl:for-each>
            <xsl:text>)</xsl:text>
        </xsl:if>
        <xsl:if test="count(subfield[@id='f']) &gt; 0">
            <xsl:text>,</xsl:text>
            <xsl:value-of select="subfield[@id='f']"/>
        </xsl:if>
        <xsl:for-each select="subfield[@id='x']">
            <xsl:text> –</xsl:text>
            <xsl:value-of select="."/>
        </xsl:for-each>
        <xsl:for-each select="subfield[@id='y']">
            <xsl:text> –</xsl:text>
            <xsl:value-of select="."/>
        </xsl:for-each>
        <xsl:for-each select="subfield[@id='z']">
            <xsl:text>,</xsl:text>
            <xsl:value-of select="."/>
        </xsl:for-each>
        <xsl:text>.</xsl:text>
    </xsl:for-each>
    <xsl:for-each select="field[@id='601']">
        <xsl:text></xsl:text>
        <xsl:value-of select="$p600 + position()"/>
        <xsl:text>.</xsl:text>
        <xsl:value-of select="subfield[@id='a']"/>
        <xsl:for-each select="subfield[@id='b']">
            <xsl:text> –</xsl:text>
            <xsl:value-of select="."/>
        </xsl:for-each>
        <xsl:if test="count(subfield[@id='e']) + count(subfield[@id='f']) &gt; 0">
            <xsl:text> (</xsl:text>
            <xsl:value-of select="subfield[@id='e']"/>
            <xsl:if test="count(subfield[@id='f']) &gt; 0">
                <xsl:text>;</xsl:text>
                <xsl:value-of select="subfield[@id='f']"/>
            </xsl:if>
            <xsl:text>)</xsl:text>
        </xsl:if>
        <xsl:for-each select="subfield[@id='x']">
            <xsl:text> –</xsl:text>
            <xsl:value-of select="."/>
        </xsl:for-each>
        <xsl:for-each select="subfield[@id='y']">
            <xsl:text> –</xsl:text>
            <xsl:value-of select="."/>
        </xsl:for-each>
        <xsl:for-each select="subfield[@id='z']">
            <xsl:text>,</xsl:text>
            <xsl:value-of select="."/>
        </xsl:for-each>
        <xsl:text>.</xsl:text>
    </xsl:for-each>
    <xsl:for-each select="field[@id='602']">
        <xsl:text></xsl:text>
        <xsl:value-of select="$p600 + $p601 + position()"/>
        <xsl:text>.</xsl:text>
        <xsl:value-of select="subfield[@id='a']"/>
        <xsl:if test="count(subfield[@id='f']) &gt; 0">
            <xsl:text>,</xsl:text>
            <xsl:value-of select="subfield[@id='f']"/>
        </xsl:if>
        <xsl:for-each select="subfield[@id='x']">
            <xsl:text> –</xsl:text>
            <xsl:value-of select="."/>
        </xsl:for-each>
        <xsl:for-each select="subfield[@id='y']">
            <xsl:text> –</xsl:text>
            <xsl:value-of select="."/>
        </xsl:for-each>
        <xsl:for-each select="subfield[@id='z']">
            <xsl:text>,</xsl:text>
            <xsl:value-of select="."/>
        </xsl:for-each>
        <xsl:text>.</xsl:text>
    </xsl:for-each>
    <xsl:for-each select="field[@id='606']">
        <xsl:text></xsl:text>
        <xsl:value-of select="$p600 + $p601 + $p602 + position()"/>
        <xsl:text>.</xsl:text>
        <xsl:value-of select="subfield[@id='a']"/>
        <xsl:for-each select="subfield[@id='x']">
            <xsl:text> –</xsl:text>
            <xsl:value-of select="."/>
        </xsl:for-each>
        <xsl:for-each select="subfield[@id='y']">
            <xsl:text> –</xsl:text>
            <xsl:value-of select="."/>
        </xsl:for-each>
        <xsl:for-each select="subfield[@id='z']">
            <xsl:text>,</xsl:text>
            <xsl:value-of select="."/>
        </xsl:for-each>
        <xsl:text>.</xsl:text>
    </xsl:for-each>
    <xsl:for-each select="field[@id='607']">
        <xsl:text></xsl:text>
        <xsl:value-of select="$p600 + $p601 + $p602 + $p606 + position()"/>
        <xsl:text>.</xsl:text>
        <xsl:value-of select="subfield[@id='a']"/>
        <xsl:for-each select="subfield[@id='x']">
            <xsl:text> –</xsl:text>
            <xsl:value-of select="."/>
        </xsl:for-each>
        <xsl:for-each select="subfield[@id='y']">
            <xsl:text> –</xsl:text>
            <xsl:value-of select="."/>
        </xsl:for-each>
        <xsl:for-each select="subfield[@id='z']">
            <xsl:text>,</xsl:text>
            <xsl:value-of select="."/>
        </xsl:for-each>
        <xsl:text>.</xsl:text>
    </xsl:for-each>
    <xsl:for-each select="field[@id='610']">
        <xsl:text></xsl:text>
        <xsl:value-of select="$p600 + $p601 + $p602 + $p606 + $p607 + position()"/>
        <xsl:text>.</xsl:text>
        <xsl:for-each select="subfield[@id='a']">
            <xsl:if test="position() != 1">
                <xsl:text>,</xsl:text>
            </xsl:if>
            <xsl:value-of select="."/>
        </xsl:for-each>
        <xsl:text>.</xsl:text>
    </xsl:for-each>
</xsl:template>

<xsl:template name="class">
    <xsl:for-each select="field[@id='675']">
        <xsl:if test="position() = 1">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_UDC']"/>
            <xsl:text></xsl:text>
        </xsl:if>
        <xsl:value-of select="subfield[@id='a']"/>
        <br/>
    </xsl:for-each>
    <xsl:for-each select="field[@id='676']">
        <xsl:if test="position() = 1">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_DDC']"/>
            <xsl:text></xsl:text>
        </xsl:if>
        <xsl:value-of select="subfield[@id='a']"/>
        <br/>
    </xsl:for-each>
    <xsl:for-each select="field[@id='680']">
        <xsl:if test="position() = 1">
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_LCC']"/>
            <xsl:text></xsl:text>
        </xsl:if>
        <xsl:value-of select="subfield[@id='a']"/>
        <xsl:value-of select="subfield[@id='b']"/>
        <br/>
    </xsl:for-each>
    <xsl:for-each select="field[@id='686']">
        <xsl:sort select="subfield[@id='2']"/>
        <xsl:if test="position() = 1 or position() != 1 and subfield[@id='2'] != preceding-sibling::field[@id='686'][position()=1]/subfield[@id='2']">
            <xsl:variable name="csystem" select="subfield[@id='2']"/>
            <xsl:choose>
                <xsl:when test="$csystem='rubbk'">
                    <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_LBC']"/>
                    <xsl:text></xsl:text>
                </xsl:when>
                <xsl:when test="$csystem='rugasnti'">
                    <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_GASNTI']"/>
                    <xsl:text></xsl:text>
                </xsl:when>
                <xsl:when test="$csystem='rueskl'">
                    <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_ESKL']"/>
                    <xsl:text></xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="$csystem"/>
                    <xsl:text></xsl:text>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:if>
        <xsl:value-of select="subfield[@id='a']"/>
        <br/>
    </xsl:for-each>
</xsl:template>

<xsl:template name="int">
    <xsl:apply-templates select="field[@id='801']"/>
</xsl:template>

<xsl:template name="notes">
    <xsl:for-each select="field[@id='300']/subfield[@id='a']">
        <xsl:text>.-</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="field[@id='301']/subfield[@id='a']">
        <xsl:text>.-</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="field[@id='302']/subfield[@id='a']">
        <xsl:text>.-</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="field[@id='305']/subfield[@id='a']">
        <xsl:text>.-</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="field[@id='309']/subfield[@id='a']">
        <xsl:text>.-</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="field[@id='311']/subfield[@id='a']">
        <xsl:text>.-</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="field[@id='313']/subfield[@id='a']">
        <xsl:text>.-</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="field[@id='316']">
        <xsl:text>.-</xsl:text>
        <xsl:value-of select="subfield[@id='a']"/>
        <xsl:text></xsl:text>
        <xsl:call-template name="org.by.code">
            <xsl:with-param name="oname" select="subfield[@id='5']"/>
        </xsl:call-template>
        <xsl:if test="count(subfield[@id='9'])">
            <xsl:text>:</xsl:text>
            <xsl:value-of select="subfield[@id='9']"/>
        </xsl:if>
    </xsl:for-each>
    <xsl:for-each select="field[@id='320']/subfield[@id='a']">
        <xsl:text>.-</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="field[@id='321']/subfield[@id='a']">
        <xsl:text>.-</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="field[@id='326']/subfield[@id='a']">
        <xsl:text>.-</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="field[@id='327']/subfield[@id='a']">
        <xsl:text>.-</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:if test="$abstract">
        <xsl:for-each select="field[@id='330']/subfield[@id='a']">
            <xsl:text>.</xsl:text>
            <p class="note">
                <xsl:value-of select="."/>
            </p>
        </xsl:for-each>
    </xsl:if>
    <xsl:for-each select="field[@id='333']/subfield[@id='a']">
        <xsl:text>.-</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="field[@id='337']/subfield[@id='a']">
        <xsl:text>.-</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
</xsl:template>

<xsl:template name="link">
    <xsl:param name="lbl"/>
    <xsl:value-of select="$lbl"/>
    <xsl:text></xsl:text>
    <xsl:choose>
        <xsl:when test="count(subfield[@id='1']/controlfield[@id='001']) &gt; 0 and $ht">
            <a href="follow+{subfield[@id='1']/controlfield[@id='001']}[1,12]+{$lang}">
                <xsl:call-template name="htitle">
                    <xsl:with-param name="r" select="."/>
                    <xsl:with-param name="na" select="false()"/>
                </xsl:call-template>
            </a>
        </xsl:when>
        <xsl:otherwise>
            <xsl:call-template name="htitle">
                <xsl:with-param name="r" select="."/>
                <xsl:with-param name="na" select="false()"/>
            </xsl:call-template>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template name="links">
<xsl:for-each select="field[@id='421']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_SUPPLEMENT']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='422']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_P_SUPPLEMENT']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='423']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_ISSUED_WITH']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='430']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_CONTINUES']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='431']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_CONTINUES_P']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='432']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_SUPERSEDES']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='433']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_SUPERSEDES_P']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='434']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_ABSORBED']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='435']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_ABSORBED_P']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='436']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="$msg/messages/localization[@language=$lang]/msg[@id='I_MERGE']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='437']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_SEPARATED']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='440']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_CONTINUED']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='441']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_CONTINUED_P']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='442']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_SUPERSEDED']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='443']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_SUPERSEDED_P']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='444']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_ABSORBED_BY']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='445']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_ABSORBED_BY_P']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='446']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="$msg/messages/localization[@language=$lang]/msg[@id='I_SPLIT']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='448']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="$msg/messages/localization[@language=$lang]/msg[@id='I_BACK']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='451']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_SAME_MEDIUM']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='452']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_ANOTHER_MEDIUM']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='453']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_TRANSLATED']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='454']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_TRANSLATION']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='455']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_REPRODUCTION']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='456']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_REPRODUCED']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='470']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_REVIEWED']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='481']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_ALSO_BOUND']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='482']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl"
                                    select="$msg/messages/localization[@language=$lang]/msg[@id='I_BOUND_WITH']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
<xsl:for-each select="field[@id='488']">
    <xsl:if test="indicator[@id='2'] = 1">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>.</xsl:text>
                <p/>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="$msg/messages/localization[@language=$lang]/msg[@id='I_OTHER']"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:call-template name="link">
                    <xsl:with-param name="lbl" select="','"/>
                </xsl:call-template>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:for-each>
</xsl:template>

<xsl:template match="field[@id='801']">
    <xsl:call-template name="org.by.code">
        <xsl:with-param name="oname" select="subfield[@id='b']"/>
    </xsl:call-template>
    <xsl:text></xsl:text>
    <xsl:variable name="date" select="subfield[@id='c']"/>
    <xsl:value-of select="substring($date, 7, 2)"/>
    <xsl:text>.</xsl:text>
    <xsl:value-of select="substring($date, 5, 2)"/>
    <xsl:text>.</xsl:text>
    <xsl:value-of select="substring($date, 1, 4)"/>
    <br/>
</xsl:template>

<xsl:template name="holdings">
    <xsl:variable name="h">
        <xsl:for-each select="field[@id='899']">
            <xsl:variable name="c" select="subfield[@id='a']"/>
            <xsl:choose>
                <xsl:when test="not($ind/ind/org[@id=$c])">
                    <org code="{$c}" weight="72"/>
                    <!-- if we have no stats for library then use default value of 72 hrs -->
                </xsl:when>
                <xsl:when test="$ind/ind/org[@id=$c]/timings = '-'">
                    <org code="{$c}" weight="1000000"/>
                </xsl:when>
                <xsl:otherwise>
                    <org code="{$c}" weight="{($ind/ind/org[@id=$c]/queue + 1) * $ind/ind/org[@id=$c]/timings}"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:for-each>
    </xsl:variable>
    <xsl:apply-templates select="exsl:node-set($h)/org">
        <xsl:sort select="@weight" data-type="number"/>
    </xsl:apply-templates>
</xsl:template>

<xsl:template match="org">
    <div id="{@code}">
        <xsl:call-template name="org.by.code">
            <xsl:with-param name="oname" select="@code"/>
        </xsl:call-template>
    </div>
</xsl:template>

<xsl:template match="field[@id='899']">
    <xsl:call-template name="org.by.code">
        <xsl:with-param name="oname" select="subfield[@id='a']"/>
    </xsl:call-template>
    <xsl:for-each select="subfield[@id='b']">
        <xsl:text></xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='c']">
        <xsl:text></xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:if test="subfield[@id='h']">
        <xsl:text></xsl:text>
        <xsl:value-of select="subfield[@id='h']"/>
    </xsl:if>
    <xsl:for-each select="subfield[@id='i']">
        <xsl:text></xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:if test="subfield[@id='j']">
        <xsl:text></xsl:text>
        <xsl:value-of select="subfield[@id='j']"/>
    </xsl:if>
    <xsl:if test="subfield[@id='p']">
        <xsl:text></xsl:text>
        <xsl:value-of select="subfield[@id='p']"/>
    </xsl:if>
    <xsl:if test="subfield[@id='t']">
        <xsl:text></xsl:text>
        <xsl:value-of select="subfield[@id='t']"/>
    </xsl:if>
    <xsl:for-each select="subfield[@id='z']">
        <xsl:text></xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <br/>
</xsl:template>

<!--
<xsl:template match="field[@id='856']">
    <xsl:if test="subfield[@id='u']">
        <xsl:text> .- &lt;URL:</xsl:text>
        <a href="{subfield[@id='u']}">
            <xsl:value-of select="subfield[@id='u']"/>
        </a>
        <xsl:text>&gt;</xsl:text>
    </xsl:if>
</xsl:template>
-->

<xsl:template match="field[@id='010']">
    <xsl:choose>
        <xsl:when test="count(subfield[@id='a']) &gt; 0">
            <xsl:text>.-ISBN</xsl:text>
            <xsl:value-of select="subfield[@id='a']"/>
            <xsl:if test="count(subfield[@id='b']) &gt; 0">
                <xsl:text>(</xsl:text>
                <xsl:value-of select="subfield[@id='b']"/>
                <xsl:text>)</xsl:text>
            </xsl:if>
            <xsl:for-each select="subfield[@id='d']">
                <xsl:text>:</xsl:text>
                <xsl:value-of select="."/>
            </xsl:for-each>
            <xsl:for-each select="subfield[@id='9']">
                <xsl:text>,</xsl:text>
                <xsl:value-of select="."/>
            </xsl:for-each>
        </xsl:when>
        <xsl:otherwise>
            <xsl:for-each select="subfield[@id='d']">
                <xsl:choose>
                    <xsl:when test="position() != 1">
                        <xsl:text>:</xsl:text>
                        <xsl:value-of select="."/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>.-</xsl:text>
                        <xsl:value-of select="."/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
            <xsl:for-each select="subfield[@id='9']">
                <xsl:text>,</xsl:text>
                <xsl:value-of select="."/>
            </xsl:for-each>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template match="field[@id='011']">
    <xsl:choose>
        <xsl:when test="count(subfield[@id='a']) &gt; 0">
            <xsl:text>.-ISSN</xsl:text>
            <xsl:value-of select="subfield[@id='a']"/>
            <xsl:if test="count(subfield[@id='b']) &gt; 0">
                <xsl:text>(</xsl:text>
                <xsl:value-of select="subfield[@id='b']"/>
                <xsl:text>)</xsl:text>
            </xsl:if>
            <xsl:for-each select="subfield[@id='d']">
                <xsl:text>:</xsl:text>
                <xsl:value-of select="."/>
            </xsl:for-each>
            <xsl:for-each select="subfield[@id='9']">
                <xsl:text>,</xsl:text>
                <xsl:value-of select="."/>
            </xsl:for-each>
        </xsl:when>
        <xsl:otherwise>
            <xsl:for-each select="subfield[@id='d']">
                <xsl:choose>
                    <xsl:when test="position() != 1">
                        <xsl:text>:</xsl:text>
                        <xsl:value-of select="."/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>.-</xsl:text>
                        <xsl:value-of select="."/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
            <xsl:for-each select="subfield[@id='9']">
                <xsl:text>,</xsl:text>
                <xsl:value-of select="."/>
            </xsl:for-each>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template match="field[@id='700']">
    <b>
        <xsl:value-of select="subfield[@id='a']"/>
        <xsl:choose>
            <xsl:when test="count(subfield[@id='g']) &gt; 0">
                <xsl:text>,</xsl:text>
                <xsl:value-of select="subfield[@id='g']"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:if test="count(subfield[@id='b']) &gt; 0">
                    <xsl:text></xsl:text>
                    <xsl:value-of select="subfield[@id='b']"/>
                </xsl:if>
            </xsl:otherwise>
        </xsl:choose>
    </b>
    <xsl:text>.</xsl:text>
</xsl:template>

<xsl:template match="field[@id='710']">
    <b>
        <xsl:value-of select="subfield[@id='a']"/>
        <xsl:for-each select="subfield[@id='b']">
            <xsl:text>.</xsl:text>
            <xsl:value-of select="."/>
        </xsl:for-each>
    </b>
    <xsl:text>.</xsl:text>
</xsl:template>

<xsl:template match="field[@id='205']">
    <xsl:text>.-</xsl:text>
    <xsl:value-of select="subfield[@id='a']"/>
    <xsl:for-each select="subfield[@id='b']">
        <xsl:text>,</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='d']">
        <xsl:text> =</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:if test="count(subfield[@id='f']) &gt; 0 or count(subfield[@id='g']) &gt; 0">
        <xsl:text> /</xsl:text>
        <xsl:for-each select="subfield[@id='f']">
            <xsl:choose>
                <xsl:when test="position() = 1">
                    <xsl:value-of select="."/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:text>;</xsl:text>
                    <xsl:value-of select="."/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:for-each>
        <xsl:for-each select="subfield[@id='g']">
            <xsl:text>;</xsl:text>
            <xsl:value-of select="."/>
        </xsl:for-each>
    </xsl:if>
</xsl:template>

<xsl:template match="field[@id='207']">
    <xsl:text>.-</xsl:text>
    <xsl:for-each select="subfield[@id='a']">
        <xsl:if test="position() != 1">
            <xsl:text>;</xsl:text>
        </xsl:if>
        <xsl:value-of select="."/>
    </xsl:for-each>
</xsl:template>

<xsl:template match="field[@id='210']">
    <xsl:text>.-</xsl:text>
    <xsl:choose>
        <xsl:when test="count(subfield[@id='a']) &gt; 0">
            <xsl:for-each select="subfield[@id='a']">
                <xsl:choose>
                    <xsl:when test="position() = 1">
                        <xsl:value-of select="."/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:text>;</xsl:text>
                        <xsl:value-of select="."/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:for-each>
        </xsl:when>
        <xsl:otherwise>
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SINE_LOCO']"/>
        </xsl:otherwise>
    </xsl:choose>
    <xsl:choose>
        <xsl:when test="count(subfield[@id='c']) &gt; 0">
            <xsl:for-each select="subfield[@id='c']">
                <xsl:text>:</xsl:text>
                <xsl:value-of select="."/>
            </xsl:for-each>
        </xsl:when>
        <xsl:otherwise>
            <xsl:text>:</xsl:text>
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SINE_NOMINE']"/>
        </xsl:otherwise>
    </xsl:choose>
    <xsl:text>,</xsl:text>
    <xsl:choose>
        <xsl:when test="count(subfield[@id='d']) &gt; 0">
            <xsl:value-of select="subfield[@id='d']"/>
        </xsl:when>
        <xsl:otherwise>
            <xsl:value-of select="$msg/messages/localization[@language=$lang]/msg[@id='I_SINE_ANNO']"/>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<xsl:template match="field[@id='215']">
    <xsl:text>.-</xsl:text>
    <xsl:for-each select="subfield[@id='a']">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:value-of select="."/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>,</xsl:text>
                <xsl:value-of select="."/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:for-each>
    <xsl:if test="count(subfield[@id='c']) &gt; 0">
        <xsl:text>:</xsl:text>
        <xsl:value-of select="subfield[@id='c']"/>
    </xsl:if>
    <xsl:for-each select="subfield[@id='d']">
        <xsl:text>;</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='e']">
        <xsl:text>+</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
</xsl:template>

<xsl:template match="field[@id='225']">
    <xsl:text>.-(</xsl:text>
    <xsl:value-of select="subfield[@id='a']"/>
    <xsl:for-each select="subfield[@id='d']">
        <xsl:text> =</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='h']">
        <xsl:text>.</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='i']">
        <xsl:choose>
            <xsl:when test="position() = 1">
                <xsl:text>,</xsl:text>
                <xsl:value-of select="."/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>.</xsl:text>
                <xsl:value-of select="."/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='e']">
        <xsl:text>:</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:if test="count(subfield[@id='f']) &gt; 0">
        <xsl:text> /</xsl:text>
        <xsl:for-each select="subfield[@id='f']">
            <xsl:choose>
                <xsl:when test="position() = 1">
                    <xsl:value-of select="."/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:text>;</xsl:text>
                    <xsl:value-of select="."/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:for-each>
    </xsl:if>
    <xsl:for-each select="subfield[@id='v']">
        <xsl:text>;</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:for-each select="subfield[@id='x']">
        <xsl:text>,</xsl:text>
        <xsl:value-of select="."/>
    </xsl:for-each>
    <xsl:text>)</xsl:text>
</xsl:template>

<xsl:template match="field[@id='230']">
    <xsl:text>.-</xsl:text>
    <xsl:value-of select="subfield[@id='a']"/>
</xsl:template>

</xsl:stylesheet>
