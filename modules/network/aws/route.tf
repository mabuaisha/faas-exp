resource "aws_route_table" "public_route_table" {
    vpc_id = aws_vpc.vpc.id

    tags {
        Name = "${var.env_name}-public-route-table"
    }
}


resource "aws_route" "public_route" {
  route_table_id = aws_vpc.vpc.main_route_table_id
  destination_cidr_block = var.public_subnet_cidr
  gateway_id = aws_internet_gateway.vpc_internet_gateway.id
}

resource "aws_route_table_association" "public_subnet_route_table_association" {
    subnet_id = aws_subnet.public_subnet.id
    route_table_id = aws_route_table.public_route_table.id
}


resource "aws_route_table" "private_route_table" {
    vpc_id = aws_vpc.vpc.id

    tags {
        Name = "${var.env_name}-private-route-table"
    }
}

resource "aws_route" "private_route" {
	route_table_id  = aws_route_table.private_route_table.id
	destination_cidr_block = var.private_subnet_cidr
	nat_gateway_id = aws_nat_gateway.app_nat_gateway.id
}



resource "aws_route_table_association" "private_subnet_route_table_association" {
    subnet_id = aws_subnet.private_subnet.id
    route_table_id = aws_route_table.private_route_table.id
}