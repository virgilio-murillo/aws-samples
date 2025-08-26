resource "aws_network_acl" "my_nacl" {
  vpc_id = aws_vpc.my_vpc.id
  tags = {
    Name = "my-nacl"
  }
}

# Inbound Allow All
resource "aws_network_acl_rule" "inbound_allow_all" {
  network_acl_id = aws_network_acl.my_nacl.id
  rule_number    = 100
  egress         = false
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
}

# Outbound Allow All
resource "aws_network_acl_rule" "outbound_allow_all" {
  network_acl_id = aws_network_acl.my_nacl.id
  rule_number    = 100
  egress         = true
  protocol       = "-1"
  rule_action    = "allow"
  cidr_block     = "0.0.0.0/0"
}

# Associations
resource "aws_network_acl_association" "public_nacl_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  network_acl_id = aws_network_acl.my_nacl.id
}

resource "aws_network_acl_association" "private_1_nacl_assoc" {
  subnet_id      = aws_subnet.private_subnet_1.id
  network_acl_id = aws_network_acl.my_nacl.id
}

resource "aws_network_acl_association" "private_2_nacl_assoc" {
  subnet_id      = aws_subnet.private_subnet_2.id
  network_acl_id = aws_network_acl.my_nacl.id
}
